from core.portfolio_engine.loader import PortfolioLoader
from core.portfolio_engine.optimizer import PortfolioOptimizer
from core.portfolio_engine.efficient_frontier import EfficientFrontier

loader = PortfolioLoader()

portfolio = loader.load([

    "AAPL",
    "MSFT",
    "GOOGL",
    "META",
    "NVDA"

])

optimizer = PortfolioOptimizer(portfolio)

frontier = EfficientFrontier(optimizer)

results = frontier.simulate(

    portfolios=1000

)

print("=" * 60)

print("Simulated:", len(results))

print("=" * 60)

best = max(

    results,

    key=lambda x: x["sharpe"]

)

print(best)