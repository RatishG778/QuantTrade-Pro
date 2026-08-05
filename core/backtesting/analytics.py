class Analytics:

    def __init__(self, equity_curve, trade_history):

        self.equity_curve = equity_curve
        self.trade_history = trade_history

    def max_drawdown(self):

        peak = self.equity_curve[0]
        max_dd = 0

        for value in self.equity_curve:

            if value > peak:
                peak = value

            drawdown = (peak - value) / peak

            if drawdown > max_dd:
                max_dd = drawdown

        return max_dd * 100

    def average_win(self):

        wins = [x for x in self.trade_history if x > 0]

        if len(wins) == 0:
            return 0

        return sum(wins) / len(wins)

    def average_loss(self):

        losses = [x for x in self.trade_history if x < 0]

        if len(losses) == 0:
            return 0

        return abs(sum(losses) / len(losses))

    def profit_factor(self):

        gross_profit = sum(x for x in self.trade_history if x > 0)

        gross_loss = abs(sum(x for x in self.trade_history if x < 0))

        if gross_loss == 0:
            return 0

        return gross_profit / gross_loss

    def risk_reward(self):

        loss = self.average_loss()

        if loss == 0:
            return 0

        return self.average_win() / loss