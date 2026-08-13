import pandas as pd

from research.portfolio.allocation import (
    AllocationEngine
)


class PortfolioOptimizer:

    def equal_weight_portfolio(
        self,
        prices: pd.DataFrame
    ) -> dict:

        if prices.empty:
            return {}

        return AllocationEngine.equal_weight(
            prices.columns
        )

    def optimize(
        self,
        returns: pd.DataFrame
    ) -> dict:

        if returns.empty:
            return {}

        assets = list(returns.columns)

        # Baseline optimizer.
        # Equal weighting provides a stable
        # benchmark before more advanced
        # optimization methods are introduced.
        return AllocationEngine.equal_weight(
            assets
        )