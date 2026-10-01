from quant.portfolio.state import PortfolioState
from backend.app.services.execution_service import ExecutionService


def test_execution_service_blocks_live_execution_by_default():
    service = ExecutionService(live_enabled=False)
    portfolio = PortfolioState(cash=1000.0)

    result = service.submit_order(
        portfolio=portfolio,
        symbol="AAPL",
        side="BUY",
        quantity=5,
        price=100.0,
        environment="LIVE",
    )

    assert result["approved"] is False
    assert result["status"] == "BLOCKED"
    assert "live" in result["reason"].lower()


def test_execution_service_allows_paper_orders_within_limits():
    service = ExecutionService(live_enabled=False)
    portfolio = PortfolioState(cash=2000.0)

    result = service.submit_order(
        portfolio=portfolio,
        symbol="AAPL",
        side="BUY",
        quantity=4,
        price=25.0,
        environment="PAPER",
    )

    assert result["approved"] is True
    assert result["status"] == "VALIDATED"
    assert result["order_value"] == 100.0


def test_execution_service_blocks_orders_that_exceed_portfolio_exposure_limit():
    service = ExecutionService(live_enabled=False, max_gross_exposure=100.0)
    portfolio = PortfolioState(cash=1000.0)
    portfolio.add_position("AAPL", 5, 10.0)

    result = service.submit_order(
        portfolio=portfolio,
        symbol="AAPL",
        side="BUY",
        quantity=3,
        price=40.0,
        environment="PAPER",
    )

    assert result["approved"] is False
    assert result["status"] == "REJECTED"
    assert "exposure" in result["reason"].lower()
