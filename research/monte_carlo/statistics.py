import numpy as np


class MonteCarloStatistics:

    @staticmethod
    def probability_of_loss(results) -> float:

        if not results:
            return 0.0

        losses = sum(
            1
            for result in results
            if result < 0
        )

        return losses / len(results) * 100

    @staticmethod
    def probability_of_profit(results) -> float:

        if not results:
            return 0.0

        profits = sum(
            1
            for result in results
            if result > 0
        )

        return profits / len(results) * 100

    @staticmethod
    def percentile(results, percentile: float) -> float:

        if not results:
            return 0.0

        return float(
            np.percentile(results, percentile)
        )