import pandas as pd
import numpy as np


class PortfolioOptimizer:

    def __init__(self, portfolio):

        self.portfolio = portfolio

    def returns(self):

        returns = pd.DataFrame()

        for symbol, df in self.portfolio.items():

            returns[symbol] = df["Close"].pct_change()

        return returns.dropna()

    def equal_weight_portfolio(self):

        returns = self.returns()

        n = len(returns.columns)

        weights = np.repeat(1 / n, n)

        expected_return = (
            returns.mean() * weights
        ).sum()

        covariance = returns.cov()

        risk = np.sqrt(
            weights.T @ covariance @ weights
        )

        return {

            "weights": dict(

                zip(

                    returns.columns,

                    weights

                )

            ),

            "expected_return": expected_return,

            "risk": risk

        }