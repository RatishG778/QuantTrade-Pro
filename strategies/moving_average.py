from strategies.base_strategy import BaseStrategy


class MovingAverageStrategy(BaseStrategy):

    def generate_signals(self):

        df = self.data.copy()

        df["Signal"] = 0

        df.loc[
            df["SMA_20"] > df["SMA_50"],
            "Signal"
        ] = 1

        df.loc[
            df["SMA_20"] < df["SMA_50"],
            "Signal"
        ] = -1

        return df