from dashboard.run_backtest import run_backtest


class AutomationEngine:

    def run(

        self,

        symbols,

        strategies,

        capital

    ):

        results = []

        for symbol in symbols:

            for strategy in strategies:

                result = run_backtest(

                    symbol,

                    capital,

                    strategy

                )

                results.append(result)

        return results