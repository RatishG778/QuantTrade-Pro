from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class BrokerAdapter(ABC):
    @abstractmethod
    def authenticate(self) -> bool:
        pass

    @abstractmethod
    def get_account(self) -> dict[str, Any]:
        pass

    @abstractmethod
    def get_positions(self) -> list[dict[str, Any]]:
        pass

    @abstractmethod
    def get_orders(self) -> list[dict[str, Any]]:
        pass

    @abstractmethod
    def get_quote(self, symbol: str) -> dict[str, Any]:
        pass

    @abstractmethod
    def place_order(self, symbol: str, side: str, quantity: int, price: float) -> dict[str, Any]:
        pass

    @abstractmethod
    def modify_order(self, order_id: str, **kwargs: Any) -> dict[str, Any]:
        pass

    @abstractmethod
    def cancel_order(self, order_id: str) -> dict[str, Any]:
        pass

    @abstractmethod
    def get_order_status(self, order_id: str) -> dict[str, Any]:
        pass


class PaperBrokerAdapter(BrokerAdapter):
    def authenticate(self) -> bool:
        return True

    def get_account(self) -> dict[str, Any]:
        return {"account_id": "paper-account", "status": "ACTIVE"}

    def get_positions(self) -> list[dict[str, Any]]:
        return []

    def get_orders(self) -> list[dict[str, Any]]:
        return []

    def get_quote(self, symbol: str) -> dict[str, Any]:
        return {"symbol": symbol, "bid": 100.0, "ask": 101.0, "last": 100.5}

    def place_order(self, symbol: str, side: str, quantity: int, price: float) -> dict[str, Any]:
        fill_price = price * 1.0002 if side.upper() == "BUY" else price * 0.9998
        return {
            "status": "SUBMITTED",
            "symbol": symbol,
            "quantity": quantity,
            "side": side.upper(),
            "price": price,
            "fill_price": fill_price,
            "order_id": f"paper-{symbol.lower()}-{quantity}",
        }

    def modify_order(self, order_id: str, **kwargs: Any) -> dict[str, Any]:
        return {"status": "MODIFIED", "order_id": order_id, **kwargs}

    def cancel_order(self, order_id: str) -> dict[str, Any]:
        return {"status": "CANCELLED", "order_id": order_id}

    def get_order_status(self, order_id: str) -> dict[str, Any]:
        return {"status": "SUBMITTED", "order_id": order_id}
