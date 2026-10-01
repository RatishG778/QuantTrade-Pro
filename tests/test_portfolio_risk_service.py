from backend.app.services.portfolio_risk_service import PortfolioRiskService


def test_portfolio_risk_service_tracks_exposure_and_thresholds():
    service = PortfolioRiskService()

    summary = service.evaluate_portfolio(
        cash=5000.0,
        positions={"AAPL": 10, "MSFT": 8},
        prices={"AAPL": 100.0, "MSFT": 90.0},
    )

    assert summary["cash"] == 5000.0
    assert summary["position_count"] == 2
    assert summary["gross_exposure"] > 0
    assert summary["risk_status"] in {"OK", "WARN", "CRITICAL"}


def test_portfolio_risk_service_blocks_over_limit_exposure():
    service = PortfolioRiskService(max_gross_exposure=1000.0)

    summary = service.evaluate_portfolio(
        cash=500.0,
        positions={"AAPL": 20},
        prices={"AAPL": 100.0},
    )

    assert summary["risk_status"] == "CRITICAL"
    assert summary["blocked"] is True
