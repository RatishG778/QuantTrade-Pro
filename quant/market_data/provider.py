from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class MarketDataProvider(ABC):
    """Abstract provider interface for market data retrieval."""

    @abstractmethod
    def get_quote(self, symbol: str, **kwargs: Any) -> Any:
        pass

    @abstractmethod
    def get_ohlcv(self, symbol: str, **kwargs: Any) -> Any:
        pass

    @abstractmethod
    def get_historical_data(self, symbol: str, **kwargs: Any) -> Any:
        pass

    @abstractmethod
    def get_market_depth(self, symbol: str, **kwargs: Any) -> Any:
        pass

    @abstractmethod
    def get_instruments(self, **kwargs: Any) -> Any:
        pass

    @abstractmethod
    def get_corporate_actions(self, symbol: str, **kwargs: Any) -> Any:
        pass

    @abstractmethod
    def get_trading_calendar(self, **kwargs: Any) -> Any:
        pass
