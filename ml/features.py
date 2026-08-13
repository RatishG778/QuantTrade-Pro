import pandas as pd


class FeatureEngineer:

    def transform(self, data: pd.DataFrame) -> pd.DataFrame:

        df = data.copy()

        df["return_1"] = df["Close"].pct_change()

        df["return_5"] = (
            df["Close"].pct_change(5)
        )

        df["ma_5"] = (
            df["Close"].rolling(5).mean()
        )

        df["ma_20"] = (
            df["Close"].rolling(20).mean()
        )

        df["ma_ratio"] = (
            df["ma_5"] / df["ma_20"]
        )

        df["target"] = (
            df["Close"].shift(-1) > df["Close"]
        ).astype(int)

        return df.dropna()