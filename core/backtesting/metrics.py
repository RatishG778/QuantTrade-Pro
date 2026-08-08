import numpy as np


class PerformanceMetrics:

    def __init__(self, trades):

        self.trades = trades

    def calculate(self):

        total_trades = len(self.trades)

        wins = len([
            t for t in self.trades
            if t > 0
        ])

        losses = len([
            t for t in self.trades
            if t <= 0
        ])

        total_profit = sum(self.trades)

        win_rate = 0.0

        if total_trades > 0:

            win_rate = (
                wins / total_trades
            ) * 100

        return {
            "total_trades": total_trades,
            "wins": wins,
            "losses": losses,
            "win_rate": win_rate,
            "profit": total_profit
        }

    def sharpe_ratio(
        self,
        risk_free_rate: float = 0.0
    ) -> float:

        if len(self.trades) < 2:
            return 0.0

        returns = np.asarray(
            self.trades,
            dtype=float
        )

        volatility = returns.std()

        if volatility == 0:
            return 0.0

        return (
            (returns.mean() - risk_free_rate)
            / volatility
        )