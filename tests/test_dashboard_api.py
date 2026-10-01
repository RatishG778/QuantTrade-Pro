from fastapi.testclient import TestClient

from backend.app.main import app


def test_overview_api_does_not_invent_unavailable_account_data():
    client = TestClient(app)
    response = client.get("/api/v1/overview")

    assert response.status_code == 200
    payload = response.json()
    assert payload["portfolio"]["net_equity"] is None
    assert payload["risk"]["status"] == "UNAVAILABLE"
    assert payload["data_status"] == "NOT_CONNECTED"
    assert payload["environment"]["live_allowed"] is False


def test_strategy_listing_api_does_not_invent_unpersisted_records():
    client = TestClient(app)
    response = client.get("/api/v1/strategies")

    assert response.status_code == 200
    payload = response.json()
    assert payload == []


def test_analysis_catalog_lists_local_historical_datasets():
    client = TestClient(app)
    response = client.get("/api/v1/analysis/catalog")

    assert response.status_code == 200
    payload = response.json()
    assert payload["source"] == "local_feature_csv"
    assert "AAPL" in payload["symbols"]


def test_analysis_report_computes_market_strategy_and_portfolio_metrics():
    client = TestClient(app)
    response = client.get("/api/v1/analysis/report?symbol=AAPL")

    assert response.status_code == 200
    payload = response.json()
    assert payload["dataset"]["rows"] > 100
    assert payload["market"]["annualized_volatility_pct"] >= 0
    assert {item["name"] for item in payload["strategies"]} == {
        "Moving Average",
        "RSI",
        "MACD",
    }
    assert len(payload["portfolio"]["correlation"]) >= 2
    assert payload["monte_carlo"]["simulations"] == 1000
    assert payload["monte_carlo_strategy"] == "Moving Average"
    assert all(len(item["equity_curve"]) > 1 for item in payload["strategies"])
    assert "not included" in payload["assumptions"]["not_included"].lower()


def test_analysis_report_rejects_unknown_symbols():
    client = TestClient(app)
    response = client.get("/api/v1/analysis/report?symbol=UNKNOWN")

    assert response.status_code == 404
