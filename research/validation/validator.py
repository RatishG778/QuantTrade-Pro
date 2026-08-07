from dashboard.run_backtest import run_backtest


class ValidationEngine:

    def validate(

        self,

        symbol,

        capital,

        strategy,

        parameters

    ):

        result = run_backtest(

            symbol=symbol,

            capital=capital,

            strategy_name=strategy,

            parameters=parameters

        )

        return {

            "profit": result.profit,

            "drawdown": result.max_drawdown,

            "trades": result.trades,

            "passed": result.profit > 0

        }