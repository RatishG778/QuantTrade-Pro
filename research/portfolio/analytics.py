import numpy as np
import pandas as pd


class PortfolioAnalytics:

    @staticmethod
    def returns(prices: pd.DataFrame) -> pd.DataFrame:
        return prices.pct_change().dropna()

    @staticmethod
    def annualized_return(
        returns: pd.Series,
        periods_per_year: int = 252
    ) -> float:

        if returns.empty:
            return 0.0

        cumulative = (1 + returns).prod()

        periods = len(returns)

        if periods == 0:
            return 0.0

        return cumulative ** (
            periods_per_year / periods
        ) - 1

    @staticmethod
    def annualized_volatility(
        returns: pd.Series,
        periods_per_year: int = 252
    ) -> float:

        if returns.empty:
            return 0.0

        return returns.std() * np.sqrt(periods_per_year)

    @staticmethod
    def sharpe_ratio(
        returns: pd.Series,
        risk_free_rate: float = 0.0,
        periods_per_year: int = 252
    ) -> float:

        if returns.empty:
            return 0.0

        volatility = (
            PortfolioAnalytics
            .annualized_volatility(
                returns,
                periods_per_year
            )
        )

        if volatility == 0:
            return 0.0

        annual_return = (
            PortfolioAnalytics
            .annualized_return(
                returns,
                periods_per_year
            )
        )

        return (
            annual_return - risk_free_rate
        ) / volatility

    @staticmethod
    def max_drawdown(returns: pd.Series) -> float:

        if returns.empty:
            return 0.0

        equity = (1 + returns).cumprod()

        peak = equity.cummax()

        drawdown = (
            equity - peak
        ) / peak

        return float(drawdown.min())