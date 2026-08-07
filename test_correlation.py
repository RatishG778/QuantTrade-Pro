from core.portfolio_engine.loader import PortfolioLoader
from core.portfolio_engine.correlation import CorrelationEngine

loader = PortfolioLoader()

portfolio = loader.load([

    "AAPL",
    "MSFT",
    "GOOGL",
    "META",
    "NVDA"

])

engine = CorrelationEngine(portfolio)

print("=" * 60)

print(engine.matrix())

print("=" * 60)

print(engine.strongest_positive())

print(engine.strongest_negative())