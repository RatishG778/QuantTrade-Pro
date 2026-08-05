class QuantTradeError(Exception):
    """Base exception for QuantTrade-Pro."""
    pass


class DataNotFoundError(QuantTradeError):
    """Raised when a required data file is missing."""
    pass


class StrategyError(QuantTradeError):
    """Raised when an invalid strategy is requested."""
    pass


class PortfolioError(QuantTradeError):
    """Raised when portfolio operations fail."""
    pass


class BacktestError(QuantTradeError):
    """Raised when a backtest cannot be completed."""
    pass