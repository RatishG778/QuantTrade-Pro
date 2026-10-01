from __future__ import annotations

from backend.app.services.broker_adapter import PaperBrokerAdapter


class PaperTradingService:
    def __init__(self, slippage_bps: int = 25, latency_ms: int = 50) -> None:
        self.slippage_bps = slippage_bps
        self.latency_ms = latency_ms
        self.broker = PaperBrokerAdapter()

    def submit_order(self, symbol: str, side: str, quantity: int, price: float) -> dict[str, object]:
        fill_slippage = price * (self.slippage_bps / 10000)
        if side.upper() == "BUY":
            execution_price = price + fill_slippage
        else:
            execution_price = price - fill_slippage

        result = self.broker.place_order(symbol, side, quantity, price)
        return {
            "approved": True,
            "status": "FILLED",
            "symbol": symbol,
            "side": side.upper(),
            "quantity": quantity,
            "price": price,
            "execution_price": execution_price,
            "fills": 1,
            "slippage_bps": self.slippage_bps,
            "latency_ms": self.latency_ms,
            **result,
        }
