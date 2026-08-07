from core.backtesting.portfolio import Portfolio
from core.backtesting.metrics import PerformanceMetrics
from core.risk.risk_manager import RiskManager
from core.risk.position_sizing import PositionSizing
from core.backtesting.broker import Broker
from core.backtesting.analytics import Analytics
from core.backtesting.result import BacktestResult

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

        

        # ---------------- Performance ----------------

        metrics = PerformanceMetrics(
            self.portfolio.get_trade_history()
        )

        

        # ---------------- Analytics ----------------

        analytics = Analytics(
            self.portfolio.equity_curve,
            self.portfolio.trade_history
        )

      

        return BacktestResult(

    data=data,

    profit=sum(self.portfolio.get_trade_history()),

    trades=len(self.portfolio.get_trade_history()),

    trade_history=self.portfolio.get_trade_history(),

    equity=self.portfolio.get_equity_curve(),

    final_capital=self.portfolio.cash,

    average_win=analytics.average_win(),

    average_loss=analytics.average_loss(),

    profit_factor=analytics.profit_factor(),

    risk_reward=analytics.risk_reward(),

    max_drawdown=analytics.max_drawdown()

)
    

    