import pandas as pd


class CorrelationEngine:

    def __init__(self, portfolio):

        self.portfolio = portfolio

    def matrix(self):

        prices = pd.DataFrame()

        for symbol, df in self.portfolio.items():

            prices[symbol] = df["Close"]

        return prices.corr()

    def strongest_positive(self):

        corr = self.matrix()

        corr = corr.where(corr != 1)

        pair = corr.stack().idxmax()

        value = corr.stack().max()

        return pair, value

    def strongest_negative(self):

        corr = self.matrix()

        corr = corr.where(corr != 1)

        pair = corr.stack().idxmin()

        value = corr.stack().min()

        return pair, value