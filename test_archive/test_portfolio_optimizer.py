from core.portfolio_engine.loader import PortfolioLoader
from core.portfolio_engine.optimizer import PortfolioOptimizer

loader = PortfolioLoader()

portfolio = loader.load(

    [

        "AAPL",

        "MSFT",

        "GOOGL",

        "META",

        "NVDA"

    ]

)

optimizer = PortfolioOptimizer(portfolio)

result = optimizer.equal_weight_portfolio()

print(result)