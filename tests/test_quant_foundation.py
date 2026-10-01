import pytest

from quant.portfolio.state import PortfolioState
from quant.risk.engine import RiskEngine, OrderDecision
from quant.strategies.base import Strategy


class ConcreteStrategy(Strategy):
    def initialize(self, context):
        return {"initialized": True}

    def on_data(self, context):
        return context

    def generate_signal(self, context):
        return 1

    def on_order_update(self, event):
        return event

    def on_trade(self, trade):
        return trade


class BrokenStrategy(Strategy):
    def initialize(self, context):
        return None


def test_strategy_contract_requires_all_methods():
    class InvalidStrategy(Strategy):
        def initialize(self, context):
            return None

        def on_data(self, context):
            return None

        def generate_signal(self, context):
            return None

        def on_order_update(self, event):
            return None

    with pytest.raises(TypeError):
        InvalidStrategy()

    strategy = ConcreteStrategy()
    assert strategy.initialize({}) == {"initialized": True}
    assert strategy.on_data({}) == {}
    assert strategy.generate_signal({}) == 1


def test_portfolio_state_tracks_cash_and_positions():
    portfolio = PortfolioState(cash=10000.0)
    portfolio.add_position("AAPL", 10, 100.0)

    assert portfolio.cash == 10000.0
    assert portfolio.positions["AAPL"].quantity == 10
    assert portfolio.positions["AAPL"].avg_price == 100.0


def test_risk_engine_rejects_over_limit_order():
    portfolio = PortfolioState(cash=2000.0)
    engine = RiskEngine(max_position_size=5, max_order_value=100.0)

    decision = engine.evaluate_order(
        portfolio,
        symbol="AAPL",
        side="BUY",
        quantity=6,
        price=25.0,
    )

    assert isinstance(decision, OrderDecision)
    assert decision.approved is False
    assert "max_position_size" in decision.reason.lower()


def test_risk_engine_allows_order_under_limits():
    portfolio = PortfolioState(cash=2000.0)
    engine = RiskEngine(max_position_size=10, max_order_value=500.0)

    decision = engine.evaluate_order(
        portfolio,
        symbol="AAPL",
        side="BUY",
        quantity=4,
        price=25.0,
    )

    assert decision.approved is True
    assert decision.reason == "approved"
