from pathlib import Path
import pandas as pd


class PortfolioLoader:

    def __init__(self):

        self.base_path = (
            Path(__file__).resolve().parent.parent.parent
            / "data"
            / "features"
        )

    def load(self, symbols):

        portfolio = {}

        for symbol in symbols:

            file_path = self.base_path / f"{symbol}.csv"

            if not file_path.exists():

                print(f"{symbol} not found.")

                continue

            portfolio[symbol] = pd.read_csv(file_path)

        return portfolio