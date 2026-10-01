from backend.app.services.paper_trading import PaperTradingService
from backend.app.services.broker_adapter import BrokerAdapter, PaperBrokerAdapter


def test_paper_trading_service_simulates_realistic_fill():
    service = PaperTradingService(slippage_bps=25, latency_ms=50)

    result = service.submit_order(
        symbol="AAPL",
        side="BUY",
        quantity=10,
        price=100.0,
    )

    assert result["approved"] is True
    assert result["fills"] >= 1
    assert result["execution_price"] > 0
    assert result["latency_ms"] == 50


def test_broker_adapter_abstract_contract_requires_methods():
    class InvalidBroker(BrokerAdapter):
        pass

    try:
        InvalidBroker()
        assert False, "Expected TypeError for incomplete broker adapter"
    except TypeError:
        pass


def test_paper_broker_adapter_returns_a_valid_order_result():
    broker = PaperBrokerAdapter()
    result = broker.place_order("AAPL", "BUY", 5, 110.0)

    assert result["status"] == "SUBMITTED"
    assert result["symbol"] == "AAPL"
    assert result["quantity"] == 5
