import pandas as pd
import pytest
from fastapi.testclient import TestClient

from backend.app.services.market_data_service import MarketDataService


def sample_prices(rows=80):
    dates = pd.bdate_range("2024-01-02", periods=rows)
    closes = pd.Series(range(100, 100 + rows), index=dates, dtype=float)
    return pd.DataFrame(
        {
            "Open": closes - 0.5,
            "High": closes + 1,
            "Low": closes - 1,
            "Close": closes,
            "Volume": 1000,
        },
        index=dates,
    )


def test_price_validation_rejects_invalid_ohlc_relationships():
    prices = sample_prices()
    prices.iloc[3, prices.columns.get_loc("Low")] = prices.iloc[3]["Close"] + 1

    result = MarketDataService.validate_prices(prices)

    assert result["passed"] is False
    assert any("OHLC relationship" in error for error in result["errors"])


def test_refresh_archives_prior_raw_data_and_writes_provenance(tmp_path):
    raw_dir = tmp_path / "raw"
    raw_dir.mkdir()
    old_raw = raw_dir / "TEST.csv"
    old_raw.write_text("old snapshot", encoding="utf-8")

    service = MarketDataService(
        data_root=tmp_path,
        downloader=lambda symbol, **kwargs: sample_prices(),
    )

    result = service.refresh("TEST", period="1y")

    assert result["status"] == "refreshed"
    assert result["symbol"] == "TEST"
    assert (tmp_path / "features" / "TEST.csv").is_file()
    assert (tmp_path / "metadata" / "market_data" / "TEST.json").is_file()
    status = service.status()
    assert status["datasets"][0]["provider"] == "Yahoo Finance via yfinance"
    assert status["datasets"][0]["adjustment"] == "auto_adjusted"
    assert status["datasets"][0]["validation"] == "passed"
    archived = list((tmp_path / "archive" / "raw").glob("TEST-*.csv"))
    assert len(archived) == 1
    assert archived[0].read_text(encoding="utf-8") == "old snapshot"


def test_refresh_does_not_write_invalid_provider_data(tmp_path):
    invalid = sample_prices()
    invalid.iloc[4, invalid.columns.get_loc("Volume")] = -1
    service = MarketDataService(
        data_root=tmp_path,
        downloader=lambda symbol, **kwargs: invalid,
    )

    with pytest.raises(ValueError, match="validation"):
        service.refresh("TEST", period="1y")

    assert not (tmp_path / "features" / "TEST.csv").exists()
    assert not (tmp_path / "metadata" / "market_data" / "TEST.json").exists()


def test_market_data_status_reports_existing_files_without_refreshing():
    from backend.app.main import app

    response = TestClient(app).get("/api/v1/market-data/status")

    assert response.status_code == 200
    payload = response.json()
    assert payload["count"] >= 1
    assert "provider" in payload["datasets"][0]
    assert "validation" in payload["datasets"][0]


def test_manual_refresh_endpoint_uses_injected_provider(tmp_path, monkeypatch):
    import backend.app.main as main

    service = MarketDataService(
        data_root=tmp_path,
        downloader=lambda symbol, **kwargs: sample_prices(),
    )
    monkeypatch.setattr(main, "market_data_service", service)
    response = TestClient(main.app).post(
        "/api/v1/market-data/refresh",
        json={"symbol": "TEST", "period": "1y"},
    )

    assert response.status_code == 200
    assert response.json()["symbol"] == "TEST"
    assert response.json()["provider"] == "Yahoo Finance via yfinance"


def test_manual_refresh_endpoint_rejects_invalid_period():
    from backend.app.main import app

    response = TestClient(app).post(
        "/api/v1/market-data/refresh",
        json={"symbol": "AAPL", "period": "20y"},
    )

    assert response.status_code == 422
