from datetime import datetime

from dashboard.run_backtest import run_backtest
from research.database.repository import ExperimentRepository


class ExperimentRunner:

    def __init__(self):
        self.repository = ExperimentRepository()

    def run(
        self,
        strategy,
        symbol,
        capital,
        parameters
    ):

        result = run_backtest(
            symbol=symbol,
            capital=capital,
            strategy_name=strategy,
            parameters=parameters
        )

        experiment = {

            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

            "strategy": strategy,

            "symbol": symbol,

            "capital": capital,

            "parameters": str(parameters),

            "profit": result.profit,

            # Temporary values until we calculate them properly
            "return_pct": (
                (result.final_capital - capital) / capital * 100
            ),

            "sharpe": 0.0,

            "max_drawdown": result.max_drawdown,

            "trades": result.trades,

            "win_rate": 0.0

        }

        self.repository.save(experiment)

        return result