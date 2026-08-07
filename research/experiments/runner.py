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

        results = run_backtest(

            symbol,

            capital,

            strategy

        )

        experiment = {

            "created_at": __import__("datetime").datetime.now(),

            "strategy": strategy,

            "symbol": symbol,

            "capital": capital,

            "parameters": str(parameters),

            "profit": results["profit"],

            "return_pct": results["return_pct"],

            "sharpe": results["sharpe"],

            "max_drawdown": results["drawdown"],

            "trades": results["trades"],

            "win_rate": results["win_rate"]

        }

        self.repository.save(experiment)

        return results