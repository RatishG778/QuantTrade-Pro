from backtesting.portfolio import Portfolio
from backtesting.metrics import PerformanceMetrics
from risk_management.risk_manager import RiskManager
from risk_management.position_sizing import PositionSizing

class BacktestEngine:

    def __init__(self, strategy, initial_capital=100000):

        self.strategy = strategy

        self.portfolio = Portfolio(initial_capital)

        self.risk_manager = RiskManager()

        self.position_sizing = PositionSizing()

    def run(self):

        data = self.strategy.generate_signals()

        for _, row in data.iterrows():

            signal = row["Signal"]
            price = row["Close"]

            if signal == 1:

                    shares = self.position_sizing.calculate_position_size(
                        capital=self.portfolio.cash,
                        entry_price=price,
                        stop_loss=price * 0.95
                    )

                    if self.risk_manager.approve_trade(self.portfolio):

                        self.portfolio.buy(price, shares)

            elif signal == -1:

                self.portfolio.sell(price)


        metrics = PerformanceMetrics(
            self.portfolio.get_trade_history()
        )

        metrics.calculate()

        return data