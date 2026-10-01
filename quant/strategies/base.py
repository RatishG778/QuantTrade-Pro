from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class Strategy(ABC):
    """Base strategy interface for backtesting, validation, paper trading, and live execution.

    Strategy implementations must be independent of the UI and broker layer.
    """

    @abstractmethod
    def initialize(self, context: Any) -> Any:
        pass

    @abstractmethod
    def on_data(self, context: Any) -> Any:
        pass

    @abstractmethod
    def generate_signal(self, context: Any) -> Any:
        pass

    @abstractmethod
    def on_order_update(self, event: Any) -> Any:
        pass

    @abstractmethod
    def on_trade(self, trade: Any) -> Any:
        pass
