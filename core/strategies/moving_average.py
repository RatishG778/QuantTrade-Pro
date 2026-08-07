from core.strategies.base_strategy import BaseStrategy

import pandas as pd


class MovingAverageStrategy(BaseStrategy):

    def __init__(
        self,
        data,
        fast=20,
        slow=50
    ):
        super().__init__(data)

        self.fast = fast
        self.slow = slow

    def generate_signals(self):

        df = self.data.copy()

        # Calculate moving averages dynamically
        df[f"SMA_{self.fast}"] = (
            df["Close"]
            .rolling(self.fast)
            .mean()
        )

        df[f"SMA_{self.slow}"] = (
            df["Close"]
            .rolling(self.slow)
            .mean()
        )

        df["Signal"] = 0

        df.loc[
            df[f"SMA_{self.fast}"] >
            df[f"SMA_{self.slow}"],
            "Signal"
        ] = 1

        df.loc[
            df[f"SMA_{self.fast}"] <
            df[f"SMA_{self.slow}"],
            "Signal"
        ] = -1

        return df