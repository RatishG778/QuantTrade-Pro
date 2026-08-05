class PortfolioAllocator:

    def __init__(self, total_capital):

        self.total_capital = total_capital

    def equal_weight(self, symbols):

        allocation = {}

        weight = 1 / len(symbols)

        for symbol in symbols:

            allocation[symbol] = {
                "weight": weight,
                "capital": self.total_capital * weight
            }

        return allocation

    def custom_weight(self, weights):

        allocation = {}

        for symbol, weight in weights.items():

            allocation[symbol] = {
                "weight": weight,
                "capital": self.total_capital * weight
            }

        return allocation