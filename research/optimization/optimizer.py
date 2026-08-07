from research.optimization.grid_search import GridSearch
from research.experiments.runner import ExperimentRunner


class Optimizer:

    def __init__(self):

        self.grid = GridSearch()

        self.runner = ExperimentRunner()

    def optimize_moving_average(

        self,

        symbol,

        capital

    ):

        parameters = self.grid.moving_average(

            range(5, 35, 5),

            range(30, 210, 10)

        )

        results = []

        print("=" * 60)
        print("OPTIMIZATION STARTED")
        print("=" * 60)

        for p in parameters:

            print(
                f"Fast={p['fast']} Slow={p['slow']}"
            )

            result = self.runner.run(

                strategy="Moving Average",

                symbol=symbol,

                capital=capital,

                parameters=p

            )

            results.append(result)

        print("=" * 60)
        print("OPTIMIZATION COMPLETED")
        print("=" * 60)

        return results