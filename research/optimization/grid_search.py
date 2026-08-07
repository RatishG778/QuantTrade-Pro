from itertools import product


class GridSearch:

    def moving_average(

        self,

        fast_range,

        slow_range

    ):

        combinations = []

        for fast, slow in product(

            fast_range,

            slow_range

        ):

            if fast < slow:

                combinations.append({

                    "fast": fast,

                    "slow": slow

                })

        return combinations