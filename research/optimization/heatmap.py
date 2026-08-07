import pandas as pd

from research.database.repository import ExperimentRepository


class HeatmapBuilder:

    def __init__(self):

        self.repo = ExperimentRepository()

    def moving_average(self):

        rows = self.repo.get_all()

        columns = [

            "ID",
            "Created",
            "Strategy",
            "Symbol",
            "Capital",
            "Parameters",
            "Profit",
            "Return",
            "Sharpe",
            "Drawdown",
            "Trades",
            "Win Rate"

        ]

        df = pd.DataFrame(rows, columns=columns)

        if df.empty:
            return pd.DataFrame()

        # Only Moving Average experiments
        df = df[df["Strategy"] == "Moving Average"].copy()

        if df.empty:
            return pd.DataFrame()

        # Extract fast / slow values
        df["Fast"] = df["Parameters"].str.extract(r"'fast':\s*(\d+)").astype(int)
        df["Slow"] = df["Parameters"].str.extract(r"'slow':\s*(\d+)").astype(int)

        return df.pivot_table(
            values="Profit",
            index="Fast",
            columns="Slow",
            aggfunc="max"
        )