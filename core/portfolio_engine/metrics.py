class PortfolioMetrics:

    def __init__(self, results):

        self.results = results

    def calculate(self):

        total_profit = 0
        total_capital = 0
        total_trades = 0

        best_stock = None
        worst_stock = None

        best_profit = float("-inf")
        worst_profit = float("inf")

        for symbol, result in self.results.items():

            profit = result["Profit"]

            total_profit += profit
            total_capital += result["Final Capital"]
            total_trades += result["Trades"]

            if profit > best_profit:
                best_profit = profit
                best_stock = symbol

            if profit < worst_profit:
                worst_profit = profit
                worst_stock = symbol

        average_profit = (
            total_profit / len(self.results)
            if self.results else 0
        )

        return {

            "Portfolio Capital": round(total_capital, 2),

            "Portfolio Profit": round(total_profit, 2),

            "Average Profit": round(average_profit, 2),

            "Total Trades": total_trades,

            "Best Stock": best_stock,

            "Worst Stock": worst_stock

        }