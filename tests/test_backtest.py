import pandas as pd

from core.backtesting.engine import BacktestEngine
from core.backtesting.result import BacktestResult


class DummyStrategy:

    def __init__(self, data):
        self.data = data

    def generate_signals(self):
        return self.data


def test_backtest_buy_and_sell(monkeypatch):

    data = pd.DataFrame({
        "Close": [100.0, 110.0],
        "Signal": [1, -1]
    })

    strategy = DummyStrategy(data)

    class FakePositionSizing:

        def calculate_position_size(
            self,
            capital,
            entry_price,
            stop_loss
        ):
            return 10

    class FakeRiskManager:

        def approve_trade(self, portfolio):
            return True

    class FakeBroker:

        def execute_buy(self, price, shares):
            return price, 0.0

        def execute_sell(self, price, shares):
            return price, 0.0

    monkeypatch.setattr(
        "core.backtesting.engine.PositionSizing",
        FakePositionSizing
    )

    monkeypatch.setattr(
        "core.backtesting.engine.RiskManager",
        FakeRiskManager
    )

    monkeypatch.setattr(
        "core.backtesting.engine.Broker",
        FakeBroker
    )

    result = BacktestEngine(
        strategy,
        initial_capital=100000
    ).run()

    assert isinstance(result, BacktestResult)

    assert result.trades == 1

    assert result.trade_history == [100.0]

    assert result.profit == 100.0

    assert result.final_capital == 100100.0

    assert result.equity == [
        100000,
        100100.0
    ]

    assert result.return_pct == 0.1

    assert result.win_rate == 100.0