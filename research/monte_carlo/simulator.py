import random


class MonteCarloSimulator:

    def simulate(
        self,
        trades,
        simulations=1000
    ):

        results = []

        for _ in range(simulations):

            shuffled = trades.copy()

            random.shuffle(shuffled)

            results.append(sum(shuffled))

        return results