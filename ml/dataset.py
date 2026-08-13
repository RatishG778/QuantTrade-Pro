import pandas as pd


class DatasetBuilder:

    def __init__(self, data):

        self.data = data.copy()

    def classification_dataset(self):

        df = self.data.copy()

        # Predict next day's movement
        df["Target"] = (
            df["Close"].shift(-1) > df["Close"]
        ).astype(int)

        df = df.dropna()

        return df

    def regression_dataset(self):

        df = self.data.copy()

        # Predict next day's close
        df["Target"] = df["Close"].shift(-1)

        df = df.dropna()

        return df