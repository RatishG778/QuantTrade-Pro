from core.backtesting.portfolio import Portfolio
from core.backtesting.metrics import PerformanceMetrics
from core.risk.risk_manager import RiskManager
from core.risk.position_sizing import PositionSizing
from core.backtesting.broker import Broker
from core.backtesting.analytics import Analytics

class BacktestEngine:

    def __init__(self, strategy, initial_capital=100000):

        self.strategy = strategy

        self.portfolio = Portfolio(initial_capital)

        self.risk_manager = RiskManager()

        self.position_sizing = PositionSizing()

        self.broker = Broker()

    def run(self):

        data = self.strategy.generate_signals()

        for _, row in data.iterrows():

            signal = row["Signal"]
            price = row["Close"]

            # BUY
            if signal == 1 and self.portfolio.position == 0:

                shares = self.position_sizing.calculate_position_size(
                    capital=self.portfolio.cash,
                    entry_price=price,
                    stop_loss=price * 0.95
                )

                if self.risk_manager.approve_trade(self.portfolio):

                    buy_price, buy_commission = self.broker.execute_buy(
                        price,
                        shares
                    )

                    self.portfolio.buy(
                        buy_price,
                        shares
                    )

            # SELL
            elif signal == -1 and self.portfolio.position > 0:

                sell_price, sell_commission = self.broker.execute_sell(
                    price,
                    self.portfolio.position
                )

                self.portfolio.sell(
                    sell_price
                )

        # ---------------- Portfolio Summary ----------------

        self.portfolio.summary()

        # ---------------- Performance ----------------

        metrics = PerformanceMetrics(
            self.portfolio.get_trade_history()
        )

        metrics.calculate()

        # ---------------- Analytics ----------------

        analytics = Analytics(
            self.portfolio.equity_curve,
            self.portfolio.trade_history
        )

        print("\n" + "=" * 50)
        print("ADVANCED ANALYTICS")
        print("=" * 50)

        print(f"Average Win      : {analytics.average_win():.2f}")
        print(f"Average Loss     : {analytics.average_loss():.2f}")
        print(f"Profit Factor    : {analytics.profit_factor():.2f}")
        print(f"Risk Reward      : {analytics.risk_reward():.2f}")
        print(f"Maximum Drawdown : {analytics.max_drawdown():.2f}%")

        return {
            "capital": self.portfolio.cash,
            "equity_curve": self.portfolio.equity_curve,
            "trade_history": self.portfolio.trade_history
}