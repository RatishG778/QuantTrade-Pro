from research.monte_carlo.metrics import MonteCarloMetrics
from research.monte_carlo.statistics import MonteCarloStatistics


class MonteCarloReport:

    def generate(self, results):

        summary = MonteCarloMetrics.summarize(
            results
        )

        summary["probability_of_profit"] = (
            MonteCarloStatistics.probability_of_profit(
                results
            )
        )

        summary["probability_of_loss"] = (
            MonteCarloStatistics.probability_of_loss(
                results
            )
        )

        return summary