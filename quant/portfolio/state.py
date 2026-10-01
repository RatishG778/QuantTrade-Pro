from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict


@dataclass
class Position:
    symbol: str
    quantity: int = 0
    avg_price: float = 0.0


@dataclass
class PortfolioState:
    cash: float = 0.0
    positions: Dict[str, Position] = field(default_factory=dict)

    def add_position(self, symbol: str, quantity: int, avg_price: float) -> Position:
        existing = self.positions.get(symbol)
        if existing is None:
            self.positions[symbol] = Position(symbol=symbol, quantity=quantity, avg_price=avg_price)
            return self.positions[symbol]

        total_quantity = existing.quantity + quantity
        existing.avg_price = (
            (existing.quantity * existing.avg_price) + (quantity * avg_price)
        ) / max(total_quantity, 1)
        existing.quantity = total_quantity
        return existing

    def remove_position(self, symbol: str, quantity: int) -> Position | None:
        existing = self.positions.get(symbol)
        if existing is None:
            return None

        remaining = existing.quantity - quantity
        if remaining <= 0:
            del self.positions[symbol]
            return existing

        existing.quantity = remaining
        return existing
