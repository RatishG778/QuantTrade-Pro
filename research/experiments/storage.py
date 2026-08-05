from pathlib import Path
import pandas as pd


class ExperimentStorage:

    def __init__(self):

        self.path = Path("research/reports")

        self.path.mkdir(parents=True, exist_ok=True)

        self.file = self.path / "experiments.csv"

    def save(self, experiment, results):

        row = {

            "Date": experiment.created_at,

            "Experiment": experiment.name,

            "Strategy": experiment.strategy,

            "Symbol": experiment.symbol,

            "Capital": experiment.capital,

            "Parameters": str(experiment.parameters),

            "Profit": results["profit"],

            "Trades": results["trades"]
        }

        if self.file.exists():

            df = pd.read_csv(self.file)

            df = pd.concat(
                [df, pd.DataFrame([row])],
                ignore_index=True
            )

        else:

            df = pd.DataFrame([row])

        df.to_csv(self.file, index=False)