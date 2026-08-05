import pandas as pd


class CorrelationEngine:

    def __init__(self, portfolio):

        self.portfolio = portfolio

    def calculate(self):

        prices = pd.DataFrame()

        for symbol, df in self.portfolio.items():

            prices[symbol] = df["Close"]

        correlation = prices.corr()

        return correlation