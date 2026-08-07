import numpy as np
import pandas as pd


class PortfolioOptimizer:

    def __init__(self, portfolio):

        self.portfolio = portfolio

    def returns(self):

        returns = pd.DataFrame()

        for symbol, df in self.portfolio.items():

            returns[symbol] = df["Close"].pct_change()

        return returns.dropna()

    def statistics(self):

        r = self.returns()

        mean = r.mean() * 252
        cov = r.cov() * 252

        return mean, cov

    def portfolio_performance(self, weights):

        mean, cov = self.statistics()

        expected_return = np.sum(mean * weights)

        risk = np.sqrt(

            weights.T @ cov @ weights

        )

        sharpe = (

            expected_return / risk

            if risk > 0 else 0

        )

        return {

            "return": expected_return,

            "risk": risk,

            "sharpe": sharpe

        }