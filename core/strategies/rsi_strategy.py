import numpy as np


class RSIStrategy:

    def __init__(self, data):
        self.data = data

    def generate_signals(self):

        df = self.data.copy()

        df["Signal"] = np.where(
            df["RSI"] < 30,
            1,
            np.where(
                df["RSI"] > 70,
                -1,
                0
            )
        )

        return df