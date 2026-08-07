from core.portfolio_engine.loader import PortfolioLoader
from core.portfolio_engine.correlation import CorrelationEngine

loader = PortfolioLoader()

portfolio = loader.load([
    "AAPL",
    "MSFT",
    "GOOGL",
    "AMZN",
    "META"
])

engine = CorrelationEngine(portfolio)

corr = engine.calculate()

print(corr)