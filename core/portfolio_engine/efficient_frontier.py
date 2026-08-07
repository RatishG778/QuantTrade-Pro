import numpy as np


class EfficientFrontier:

    def __init__(self, optimizer):

        self.optimizer = optimizer

    def simulate(

        self,

        portfolios=10000

    ):

        mean, cov = self.optimizer.statistics()

        assets = len(mean)

        results = []

        for _ in range(portfolios):

            weights = np.random.random(assets)

            weights /= np.sum(weights)

            expected_return = np.sum(mean * weights)

            risk = np.sqrt(

                weights.T @ cov @ weights

            )

            sharpe = (

                expected_return / risk

                if risk > 0 else 0

            )

            results.append({

                "weights": weights,

                "return": expected_return,

                "risk": risk,

                "sharpe": sharpe

            })

        return results