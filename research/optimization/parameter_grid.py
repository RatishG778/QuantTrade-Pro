from itertools import product


class ParameterGrid:

    def moving_average(self):

        fast = [5, 10, 15, 20, 25]

        slow = [30, 50, 75, 100, 150]

        grid = []

        for f, s in product(fast, slow):

            if f < s:

                grid.append({

                    "fast": f,

                    "slow": s

                })

        return grid
    