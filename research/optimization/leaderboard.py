import pandas as pd

from research.database.repository import ExperimentRepository


class Leaderboard:

    def __init__(self):

        self.repo = ExperimentRepository()

    def by_profit(self):

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
            return df

        return df.sort_values(
            by="Profit",
            ascending=False
        )