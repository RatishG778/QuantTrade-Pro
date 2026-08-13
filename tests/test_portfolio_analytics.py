import pandas as pd

from research.portfolio.analytics import (
    PortfolioAnalytics
)
from research.portfolio.correlation import (
    CorrelationAnalyzer
)
from research.portfolio.allocation import (
    AllocationEngine
)
from research.portfolio.optimizer import (
    PortfolioOptimizer
)


def test_portfolio_returns():

    prices = pd.DataFrame({
        "A": [100, 110, 121],
        "B": [100, 105, 110]
    })

    returns = PortfolioAnalytics.returns(prices)

    assert len(returns) == 2
    assert "A" in returns.columns
    assert "B" in returns.columns


def test_correlation():

    prices = pd.DataFrame({
        "A": [100, 110, 120, 130],
        "B": [100, 105, 110, 115]
    })

    correlation = CorrelationAnalyzer().calculate(
        prices
    )

    assert correlation.shape == (2, 2)
    assert correlation.loc["A", "A"] == 1.0


def test_equal_weight():

    weights = AllocationEngine.equal_weight(
        ["A", "B", "C"]
    )

    assert len(weights) == 3
    assert sum(weights.values()) == 1.0


def test_portfolio_optimizer():

    prices = pd.DataFrame({
        "A": [100, 110, 120],
        "B": [100, 105, 110]
    })

    weights = PortfolioOptimizer().equal_weight_portfolio(
        prices
    )

    assert len(weights) == 2
    assert sum(weights.values()) == 1.0