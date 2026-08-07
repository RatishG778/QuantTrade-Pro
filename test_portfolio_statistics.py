import numpy as np

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

weights = np.array(

    [

        0.2,

        0.2,

        0.2,

        0.2,

        0.2

    ]

)

print(

    optimizer.portfolio_performance(weights)

)