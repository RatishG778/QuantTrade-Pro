from dashboard.run_backtest import run_backtest

from research.experiments.storage import ExperimentStorage


class ExperimentRunner:

    def __init__(self):

        self.storage = ExperimentStorage()

    def run(self, experiment):

        results = run_backtest(

            experiment.symbol,

            experiment.capital,

            experiment.strategy

        )

        self.storage.save(

            experiment,

            results

        )

        return results