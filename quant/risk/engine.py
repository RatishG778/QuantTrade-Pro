from __future__ import annotations

from dataclasses import dataclass

from quant.portfolio.state import PortfolioState


@dataclass
class OrderDecision:
    approved: bool
    reason: str = "approved"


class RiskEngine:
    def __init__(
        self,
        max_position_size: int = 10,
        max_order_value: float = 500.0,
        max_daily_loss: float = 0.0,
    ) -> None:
        self.max_position_size = max_position_size
        self.max_order_value = max_order_value
        self.max_daily_loss = max_daily_loss

    def evaluate_order(
        self,
        portfolio: PortfolioState,
        symbol: str,
        side: str,
        quantity: int,
        price: float,
    ) -> OrderDecision:
        if quantity <= 0:
            return OrderDecision(False, "quantity must be positive")

        if side.upper() not in {"BUY", "SELL"}:
            return OrderDecision(False, "unsupported order side")

        order_value = quantity * price
        if quantity > self.max_position_size:
            return OrderDecision(False, "max_position_size exceeded")

        if order_value > self.max_order_value:
            return OrderDecision(False, "max_order_value exceeded")

        if side.upper() == "BUY" and portfolio.cash < order_value:
            return OrderDecision(False, "insufficient cash")

        if self.max_daily_loss and portfolio.cash < 0:
            return OrderDecision(False, "daily loss limit reached")

        return OrderDecision(True, "approved")
