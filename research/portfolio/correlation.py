import pandas as pd


class CorrelationAnalyzer:

    def calculate(
        self,
        prices: pd.DataFrame
    ) -> pd.DataFrame:

        returns = prices.pct_change().dropna()

        if returns.empty:
            return pd.DataFrame()

        return returns.corr()