from pathlib import Path
import pandas as pd
from core.exceptions import DataNotFoundError


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

               raise DataNotFoundError(
                   f"Data file not found: {file_path}"
                )

            portfolio[symbol] = pd.read_csv(file_path)

        return portfolio