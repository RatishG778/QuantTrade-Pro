from dashboard.run_backtest import run_backtest
from research.experiments.runner import ExperimentRunner


class ResearchPipeline:

    def __init__(self):

        self.runner = ExperimentRunner()

    def execute(

        self,

        symbol,

        strategy,

        capital,

        parameters=None

    ):

        if parameters is None:

            parameters = {}

        result = self.runner.run(

            strategy=strategy,

            symbol=symbol,

            capital=capital,

            parameters=parameters

        )

        return result