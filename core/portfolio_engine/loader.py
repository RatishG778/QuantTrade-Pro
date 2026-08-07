from pathlib import Path
import pandas as pd

from core.exceptions import DataNotFoundError


class PortfolioLoader:

    def __init__(self):

        self.base = (
            Path(__file__).resolve()
            .parent.parent.parent
            / "data"
            / "features"
        )

    def load(self, symbols):

        portfolio = {}

        for symbol in symbols:

            file = self.base / f"{symbol}.csv"

            if not file.exists():

                raise DataNotFoundError(
                    f"Data file not found: {file}"
                )

            portfolio[symbol] = pd.read_csv(file)

        return portfolio