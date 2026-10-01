from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from config.settings import COMMISSION, SLIPPAGE
from core.strategies.strategy_factory import StrategyFactory
from research.portfolio.analytics import PortfolioAnalytics


PROJECT_ROOT = Path(__file__).resolve().parents[3]
FEATURES_DIR = PROJECT_ROOT / "data" / "features"
STRATEGIES = ("Moving Average", "RSI", "MACD")
MONTE_CARLO_SIMULATIONS = 1000


class ResearchAnalyticsService:
    def __init__(self, features_dir: Path = FEATURES_DIR) -> None:
        self.features_dir = features_dir

    def catalog(self) -> dict[str, Any]:
        datasets = []
        for path in sorted(self.features_dir.glob("*.csv")):
            frame = pd.read_csv(path, usecols=["Date"])
            dates = pd.to_datetime(frame["Date"], errors="coerce").dropna()
            datasets.append(
                {
                    "symbol": path.stem,
                    "rows": int(len(frame)),
                    "start_date": dates.min().date().isoformat() if not dates.empty else None,
                    "end_date": dates.max().date().isoformat() if not dates.empty else None,
                }
            )
        return {
            "source": "local_feature_csv",
            "symbols": [item["symbol"] for item in datasets],
            "datasets": datasets,
            "analyses": {
                "market_and_technical": "available",
                "strategy_comparison": "available",
                "portfolio_correlation": "available",
                "monte_carlo": "available",
                "parameter_optimization": "not_connected",
                "walk_forward_validation": "not_implemented",
                "machine_learning": "no_labeled_target",
            },
        }

    def report(self, symbol: str, selected_strategy: str) -> dict[str, Any]:
        normalized_symbol = symbol.strip().upper()
        if selected_strategy not in STRATEGIES:
            raise ValueError(f"Unsupported strategy: {selected_strategy}")

        available_symbols = {path.stem for path in self.features_dir.glob("*.csv")}
        if normalized_symbol not in available_symbols:
            raise KeyError(f"No local feature dataset for {normalized_symbol}")

        data = self._load_dataset(normalized_symbol)
        market_returns = data["Close"].pct_change().dropna()
        strategy_results = [
            self._strategy_result(data, strategy_name)
            for strategy_name in STRATEGIES
        ]
        selected_result = next(
            result for result in strategy_results if result["name"] == selected_strategy
        )

        all_prices = {
            path.stem: self._load_dataset(path.stem).set_index("Date")["Close"]
            for path in sorted(self.features_dir.glob("*.csv"))
        }
        price_frame = pd.concat(all_prices, axis=1).dropna()
        portfolio_returns = price_frame.pct_change().dropna().mean(axis=1)
        correlations = price_frame.pct_change().dropna().corr()
        monte_carlo = self._monte_carlo(selected_result["daily_returns"], normalized_symbol, selected_strategy)

        return {
            "data_status": "LOCAL_HISTORICAL",
            "dataset": {
                "symbol": normalized_symbol,
                "source": "data/features CSV",
                "rows": int(len(data)),
                "start_date": data["Date"].iloc[0].date().isoformat(),
                "end_date": data["Date"].iloc[-1].date().isoformat(),
            },
            "market": self._performance(market_returns),
            "risk": self._tail_risk(market_returns),
            "technical": self._technical_snapshot(data),
            "strategies": [
                {key: value for key, value in result.items() if key != "daily_returns"}
                for result in strategy_results
            ],
            "portfolio": {
                "symbols": list(price_frame.columns),
                "equal_weight": self._performance(portfolio_returns),
                "correlation": {
                    str(column): {
                        str(row): self._safe_float(correlations.loc[row, column])
                        for row in correlations.index
                    }
                    for column in correlations.columns
                },
            },
            "monte_carlo": monte_carlo,
            "monte_carlo_strategy": selected_strategy,
            "assumptions": {
                "signal_timing": "Signals are lagged one bar before returns are applied.",
                "transaction_cost_pct_per_turnover": (COMMISSION + SLIPPAGE) * 100,
                "monte_carlo": "252-trading-day bootstrap with replacement from historical strategy returns.",
                "not_included": "Not included: taxes, market impact, borrow costs, and broker fills.",
            },
        }

    def _load_dataset(self, symbol: str) -> pd.DataFrame:
        path = self.features_dir / f"{symbol}.csv"
        frame = pd.read_csv(path)
        required_columns = {"Date", "Close", "RSI", "MACD", "MACD_SIGNAL", "ATR"}
        missing = required_columns.difference(frame.columns)
        if missing:
            raise ValueError(f"Dataset {symbol} is missing required columns: {', '.join(sorted(missing))}")

        frame["Date"] = pd.to_datetime(frame["Date"], errors="coerce")
        frame["Close"] = pd.to_numeric(frame["Close"], errors="coerce")
        frame = frame.dropna(subset=["Date", "Close"]).sort_values("Date").reset_index(drop=True)
        frame = frame.loc[frame["Close"] > 0].copy()
        if len(frame) < 2:
            raise ValueError(f"Dataset {symbol} has insufficient valid price history")
        return frame

    def _strategy_result(self, data: pd.DataFrame, strategy_name: str) -> dict[str, Any]:
        signal_frame = StrategyFactory.get_strategy(strategy_name, data.copy()).generate_signals()
        signals = pd.to_numeric(signal_frame["Signal"], errors="coerce").fillna(0)
        target_position = signals.mask(signals == 0).ffill().fillna(0).clip(0, 1)
        position = target_position.shift(1).fillna(0)
        market_returns = data["Close"].pct_change().fillna(0)
        turnover = position.diff().abs()
        turnover.iloc[0] = abs(float(position.iloc[0]))
        daily_returns = (position * market_returns) - (turnover * (COMMISSION + SLIPPAGE))
        metrics = self._performance(daily_returns.iloc[1:])
        entries = position.diff().fillna(position.iloc[0]).gt(0).sum()
        points = self._curve_points(data["Date"], daily_returns)
        return {
            "name": strategy_name,
            "total_return_pct": metrics["total_return_pct"],
            "annualized_return_pct": metrics["annualized_return_pct"],
            "annualized_volatility_pct": metrics["annualized_volatility_pct"],
            "sharpe_ratio": metrics["sharpe_ratio"],
            "max_drawdown_pct": metrics["max_drawdown_pct"],
            "trade_entries": int(entries),
            "equity_curve": points,
            "daily_returns": daily_returns.iloc[1:].to_numpy(dtype=float),
        }

    @staticmethod
    def _performance(returns: pd.Series) -> dict[str, float]:
        clean = pd.to_numeric(returns, errors="coerce").dropna().astype(float)
        if clean.empty:
            return {
                "total_return_pct": 0.0,
                "annualized_return_pct": 0.0,
                "annualized_volatility_pct": 0.0,
                "sharpe_ratio": 0.0,
                "max_drawdown_pct": 0.0,
            }

        growth = (1 + clean).cumprod()
        total_return = (growth.iloc[-1] - 1) * 100
        annualized_return = PortfolioAnalytics.annualized_return(clean) * 100
        annualized_volatility = PortfolioAnalytics.annualized_volatility(clean) * 100
        sharpe_ratio = (
            PortfolioAnalytics.sharpe_ratio(clean)
            if annualized_volatility > 0
            else 0.0
        )
        max_drawdown = PortfolioAnalytics.max_drawdown(clean) * 100
        return {
            "total_return_pct": ResearchAnalyticsService._safe_float(total_return),
            "annualized_return_pct": ResearchAnalyticsService._safe_float(annualized_return),
            "annualized_volatility_pct": ResearchAnalyticsService._safe_float(annualized_volatility),
            "sharpe_ratio": ResearchAnalyticsService._safe_float(sharpe_ratio),
            "max_drawdown_pct": ResearchAnalyticsService._safe_float(max_drawdown),
        }

    @staticmethod
    def _tail_risk(returns: pd.Series) -> dict[str, float]:
        clean = pd.to_numeric(returns, errors="coerce").dropna().to_numpy(dtype=float)
        if clean.size == 0:
            return {"var_95_daily_pct": 0.0, "cvar_95_daily_pct": 0.0}
        var = float(np.percentile(clean, 5))
        tail = clean[clean <= var]
        return {
            "var_95_daily_pct": ResearchAnalyticsService._safe_float(var * 100),
            "cvar_95_daily_pct": ResearchAnalyticsService._safe_float(tail.mean() * 100),
        }

    @staticmethod
    def _technical_snapshot(data: pd.DataFrame) -> dict[str, Any]:
        last = data.iloc[-1]
        result: dict[str, Any] = {"close": ResearchAnalyticsService._safe_float(last["Close"])}
        for column in ("SMA_20", "SMA_50", "RSI", "MACD", "MACD_SIGNAL", "ATR", "Daily_Return"):
            if column in data.columns:
                result[column.lower()] = ResearchAnalyticsService._safe_float(last[column])
        return result

    @staticmethod
    def _curve_points(dates: pd.Series, daily_returns: pd.Series) -> list[dict[str, Any]]:
        equity = (1 + daily_returns.astype(float)).cumprod() * 100
        if equity.empty:
            return []
        indices = np.unique(np.linspace(0, len(equity) - 1, min(90, len(equity)), dtype=int))
        return [
            {"date": dates.iloc[index].date().isoformat(), "value": ResearchAnalyticsService._safe_float(equity.iloc[index])}
            for index in indices
        ]

    @staticmethod
    def _monte_carlo(returns: np.ndarray, symbol: str, strategy: str) -> dict[str, Any]:
        sample = np.asarray(returns, dtype=float)
        sample = sample[np.isfinite(sample)]
        if sample.size == 0:
            distribution = np.zeros(MONTE_CARLO_SIMULATIONS)
        else:
            seed = sum(ord(character) for character in f"{symbol}:{strategy}")
            generator = np.random.default_rng(seed)
            draws = generator.choice(sample, size=(MONTE_CARLO_SIMULATIONS, 252), replace=True)
            distribution = (np.prod(1 + draws, axis=1) - 1) * 100
        p5, median, p95 = np.percentile(distribution, [5, 50, 95])
        return {
            "simulations": MONTE_CARLO_SIMULATIONS,
            "horizon_trading_days": 252,
            "probability_of_loss_pct": ResearchAnalyticsService._safe_float((distribution < 0).mean() * 100),
            "p5_return_pct": ResearchAnalyticsService._safe_float(p5),
            "median_return_pct": ResearchAnalyticsService._safe_float(median),
            "p95_return_pct": ResearchAnalyticsService._safe_float(p95),
        }

    @staticmethod
    def _safe_float(value: Any) -> float | None:
        converted = float(value)
        return converted if np.isfinite(converted) else None