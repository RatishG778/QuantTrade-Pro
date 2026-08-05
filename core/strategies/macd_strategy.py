import numpy as np


class MACDStrategy:

    def __init__(self, data):
        self.data = data

    def generate_signals(self):

        df = self.data.copy()

        df["Signal"] = np.where(
            df["MACD"] > df["MACD_SIGNAL"],
            1,
            -1
        )

        return df