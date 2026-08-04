class PerformanceMetrics:

    def __init__(self, trades):

        self.trades = trades

    def calculate(self):

        total_trades = len(self.trades)

        wins = len([t for t in self.trades if t > 0])

        losses = len([t for t in self.trades if t <= 0])

        total_profit = sum(self.trades)

        win_rate = 0

        if total_trades > 0:

            win_rate = wins / total_trades * 100

        print("\n")

        print("=" * 50)

        print("Performance Report")

        print("=" * 50)

        print(f"Total Trades : {total_trades}")

        print(f"Wins         : {wins}")

        print(f"Losses       : {losses}")

        print(f"Win Rate     : {win_rate:.2f}%")

        print(f"Net Profit   : {total_profit:.2f}")