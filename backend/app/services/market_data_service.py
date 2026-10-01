from __future__ import annotations

import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

import numpy as np
import pandas as pd
import ta


PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATA_ROOT = PROJECT_ROOT / "data"
VALID_PERIODS = {"1y", "2y", "5y"}
PRICE_COLUMNS = ("Open", "High", "Low", "Close", "Volume")
SYMBOL_PATTERN = re.compile(r"^[A-Z0-9][A-Z0-9.\-]{0,11}$")


class MarketDataService:
    def __init__(
        self,
        data_root: Path = DATA_ROOT,
        downloader: Callable[..., pd.DataFrame] | None = None,
    ) -> None:
        self.data_root = Path(data_root)
        self.downloader = downloader

    def status(self) -> dict[str, Any]:
        raw_dir = self.data_root / "raw"
        manifest_dir = self.data_root / "metadata" / "market_data"
        datasets = []

        for path in sorted(raw_dir.glob("*.csv")):
            try:
                prices = self._normalize_prices(pd.read_csv(path))
                validation = self.validate_prices(prices)
                last_date = validation["end_date"]
                age_days = None
                if last_date:
                    age_days = max(
                        0,
                        (datetime.now(timezone.utc).date() - datetime.fromisoformat(last_date).date()).days,
                    )
                manifest_path = manifest_dir / f"{path.stem}.json"
                manifest = json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.exists() else {}
                datasets.append(
                    {
                        "symbol": path.stem,
                        "rows": validation["rows"],
                        "start_date": validation["start_date"],
                        "end_date": last_date,
                        "age_calendar_days": age_days,
                        "validation": "passed" if validation["passed"] else "failed",
                        "errors": validation["errors"],
                        "warnings": validation["warnings"],
                        "provider": manifest.get("provider", "unverified local file"),
                        "retrieved_at_utc": manifest.get("retrieved_at_utc"),
                        "adjustment": manifest.get("adjustment", "unknown"),
                    }
                )
            except (OSError, ValueError, pd.errors.ParserError) as error:
                datasets.append(
                    {
                        "symbol": path.stem,
                        "rows": 0,
                        "validation": "failed",
                        "errors": [str(error)],
                        "warnings": [],
                        "provider": "unverified local file",
                        "retrieved_at_utc": None,
                        "adjustment": "unknown",
                    }
                )

        return {"datasets": datasets, "count": len(datasets)}

    def refresh(self, symbol: str, period: str = "5y") -> dict[str, Any]:
        normalized_symbol = symbol.strip().upper()
        if not SYMBOL_PATTERN.fullmatch(normalized_symbol):
            raise ValueError("Symbol must contain only letters, digits, dots, or hyphens")
        if period not in VALID_PERIODS:
            raise ValueError(f"Period must be one of: {', '.join(sorted(VALID_PERIODS))}")

        download = self.downloader or self._yfinance_download
        try:
            downloaded = download(
                normalized_symbol,
                period=period,
                auto_adjust=True,
                progress=False,
                group_by="column",
                multi_level_index=False,
                threads=False,
            )
        except Exception as error:
            raise RuntimeError(f"Historical data provider failed for {normalized_symbol}: {error}") from error

        prices = self._normalize_prices(downloaded)
        validation = self.validate_prices(prices)
        if not validation["passed"]:
            problems = "; ".join(validation["errors"])
            raise ValueError(f"Downloaded data failed validation: {problems}")

        prices["Date"] = pd.to_datetime(prices["Date"], errors="coerce", utc=True).dt.tz_convert(None)
        for column in PRICE_COLUMNS:
            prices[column] = pd.to_numeric(prices[column], errors="raise")
        prices = prices.sort_values("Date").reset_index(drop=True)
        features = self._build_features(prices)
        retrieved_at = datetime.now(timezone.utc)
        raw_path = self.data_root / "raw" / f"{normalized_symbol}.csv"
        processed_path = self.data_root / "processed" / f"{normalized_symbol}.csv"
        features_path = self.data_root / "features" / f"{normalized_symbol}.csv"
        manifest_path = self.data_root / "metadata" / "market_data" / f"{normalized_symbol}.json"

        if raw_path.exists():
            archive_name = f"{normalized_symbol}-{retrieved_at.strftime('%Y%m%dT%H%M%S%fZ')}.csv"
            archive_path = self.data_root / "archive" / "raw" / archive_name
            archive_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(raw_path, archive_path)

        self._atomic_csv(prices, raw_path)
        self._atomic_csv(prices, processed_path)
        self._atomic_csv(features, features_path)

        manifest = {
            "symbol": normalized_symbol,
            "provider": "Yahoo Finance via yfinance",
            "provider_version": self._provider_version(),
            "retrieved_at_utc": retrieved_at.isoformat(),
            "requested_period": period,
            "adjustment": "auto_adjusted",
            "rows": validation["rows"],
            "start_date": validation["start_date"],
            "end_date": validation["end_date"],
            "validation": validation,
            "feature_schema_version": 1,
        }
        self._atomic_json(manifest, manifest_path)

        return {
            "status": "refreshed",
            "symbol": normalized_symbol,
            "rows": validation["rows"],
            "start_date": validation["start_date"],
            "end_date": validation["end_date"],
            "retrieved_at_utc": retrieved_at.isoformat(),
            "provider": manifest["provider"],
            "adjustment": manifest["adjustment"],
            "warnings": validation["warnings"],
        }

    @staticmethod
    def validate_prices(prices: pd.DataFrame) -> dict[str, Any]:
        errors: list[str] = []
        warnings: list[str] = []
        if prices.empty:
            return {
                "passed": False,
                "rows": 0,
                "start_date": None,
                "end_date": None,
                "errors": ["Dataset is empty"],
                "warnings": [],
            }

        prices = MarketDataService._normalize_prices(prices)
        missing_columns = set(PRICE_COLUMNS + ("Date",)).difference(prices.columns)
        if missing_columns:
            return {
                "passed": False,
                "rows": int(len(prices)),
                "start_date": None,
                "end_date": None,
                "errors": [f"Missing columns: {', '.join(sorted(missing_columns))}"],
                "warnings": [],
            }

        frame = prices.copy()
        frame["Date"] = pd.to_datetime(frame["Date"], errors="coerce", utc=True).dt.tz_convert(None)
        if frame["Date"].isna().any():
            errors.append("Dates contain invalid or missing values")
        valid_dates = frame["Date"].dropna()
        if valid_dates.duplicated().any():
            errors.append("Dates contain duplicates")
        if not valid_dates.is_monotonic_increasing:
            warnings.append("Rows are not sorted by date; ingestion will sort them")

        for column in PRICE_COLUMNS:
            frame[column] = pd.to_numeric(frame[column], errors="coerce")
            values = frame[column].to_numpy(dtype=float)
            if not np.isfinite(values).all():
                errors.append(f"{column} contains missing or non-finite values")

        if not errors:
            invalid_price = (frame[["Open", "High", "Low", "Close"]] <= 0).any(axis=None)
            if invalid_price:
                errors.append("Prices must be positive")
            inconsistent = (
                (frame["High"] < frame[["Open", "Close", "Low"]].max(axis=1))
                | (frame["Low"] > frame[["Open", "Close", "High"]].min(axis=1))
            )
            if inconsistent.any():
                errors.append("OHLC relationship is inconsistent")
            if (frame["Volume"] < 0).any():
                errors.append("Volume cannot be negative")

        ordered_dates = valid_dates.sort_values()
        if len(ordered_dates) > 1:
            gaps = ordered_dates.diff().dt.days
            if (gaps > 7).any():
                warnings.append("Date coverage contains gaps longer than seven calendar days")

        return {
            "passed": not errors,
            "rows": int(len(frame)),
            "start_date": ordered_dates.iloc[0].date().isoformat() if not ordered_dates.empty else None,
            "end_date": ordered_dates.iloc[-1].date().isoformat() if not ordered_dates.empty else None,
            "errors": errors,
            "warnings": warnings,
        }

    @staticmethod
    def _normalize_prices(prices: pd.DataFrame) -> pd.DataFrame:
        if prices is None or prices.empty:
            return pd.DataFrame(columns=("Date",) + PRICE_COLUMNS)
        frame = prices.copy()

        if isinstance(frame.columns, pd.MultiIndex):
            wanted = set(PRICE_COLUMNS)
            for level in range(frame.columns.nlevels):
                labels = set(map(str, frame.columns.get_level_values(level)))
                if wanted.issubset(labels):
                    frame.columns = frame.columns.get_level_values(level)
                    break
            else:
                frame.columns = ["_".join(map(str, column)) for column in frame.columns]

        if "Date" not in frame.columns:
            frame = frame.rename_axis("Date").reset_index()
            if "Date" not in frame.columns:
                frame = frame.rename(columns={frame.columns[0]: "Date"})

        frame.columns = [str(column).strip().title() if str(column).lower() != "macd_signal" else "MACD_SIGNAL" for column in frame.columns]
        frame = frame.loc[:, ~frame.columns.duplicated()]
        if "Date" in frame.columns:
            frame["Date"] = pd.to_datetime(frame["Date"], errors="coerce", utc=True).dt.tz_convert(None)
        for column in PRICE_COLUMNS:
            if column in frame.columns:
                frame[column] = pd.to_numeric(frame[column], errors="coerce")
        return frame

    @staticmethod
    def _build_features(prices: pd.DataFrame) -> pd.DataFrame:
        frame = prices.copy()
        close = frame["Close"]
        frame["SMA_20"] = ta.trend.sma_indicator(close, window=20)
        frame["SMA_50"] = ta.trend.sma_indicator(close, window=50)
        frame["EMA_20"] = ta.trend.ema_indicator(close, window=20)
        frame["RSI"] = ta.momentum.rsi(close, window=14)
        frame["MACD"] = ta.trend.macd(close)
        frame["MACD_SIGNAL"] = ta.trend.macd_signal(close)
        frame["BB_UPPER"] = ta.volatility.bollinger_hband(close)
        frame["BB_LOWER"] = ta.volatility.bollinger_lband(close)
        frame["ATR"] = ta.volatility.average_true_range(frame["High"], frame["Low"], close)
        frame["Daily_Return"] = close.pct_change()
        frame["Log_Return"] = np.log(close / close.shift(1))
        frame["Volatility"] = frame["Daily_Return"].rolling(20).std()
        return frame

    @staticmethod
    def _atomic_csv(frame: pd.DataFrame, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        temp_path = path.with_name(f".{path.name}.tmp")
        frame.to_csv(temp_path, index=False, date_format="%Y-%m-%d")
        temp_path.replace(path)

    @staticmethod
    def _atomic_json(payload: dict[str, Any], path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        temp_path = path.with_name(f".{path.name}.tmp")
        temp_path.write_text(json.dumps(payload, indent=2, allow_nan=False), encoding="utf-8")
        temp_path.replace(path)

    @staticmethod
    def _yfinance_download(symbol: str, **kwargs: Any) -> pd.DataFrame:
        import yfinance as yf

        return yf.download(symbol, **kwargs)

    @staticmethod
    def _provider_version() -> str:
        try:
            import yfinance as yf

            return yf.__version__
        except ImportError:
            return "unavailable"