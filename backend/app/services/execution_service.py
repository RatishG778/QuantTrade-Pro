from __future__ import annotations

from quant.portfolio.state import PortfolioState
from quant.risk.engine import RiskEngine

from backend.app.services.portfolio_risk_service import PortfolioRiskService


class ExecutionService:
    def __init__(
        self,
        live_enabled: bool = False,
        max_position_size: int = 10,
        max_order_value: float = 500.0,
        max_gross_exposure: float = 5000.0,
    ) -> None:
        self.live_enabled = live_enabled
        self.risk_engine = RiskEngine(
            max_position_size=max_position_size,
            max_order_value=max_order_value,
        )
        self.portfolio_risk_service = PortfolioRiskService(
            max_gross_exposure=max_gross_exposure,
        )

    def submit_order(
        self,
        portfolio: PortfolioState,
        symbol: str,
        side: str,
        quantity: int,
        price: float,
        environment: str = "PAPER",
    ) -> dict[str, object]:
        if environment.upper() == "LIVE" and not self.live_enabled:
            return {
                "approved": False,
                "status": "BLOCKED",
                "reason": "LIVE execution is disabled by policy.",
                "order_value": quantity * price,
            }

        decision = self.risk_engine.evaluate_order(
            portfolio=portfolio,
            symbol=symbol,
            side=side,
            quantity=quantity,
            price=price,
        )

        if not decision.approved:
            return {
                "approved": False,
                "status": "REJECTED",
                "reason": decision.reason,
                "order_value": quantity * price,
            }

        current_exposure = 0.0
        for position in portfolio.positions.values():
            current_exposure += abs(position.quantity) * position.avg_price

        existing_position = portfolio.positions.get(symbol)
        existing_quantity = existing_position.quantity if existing_position else 0
        projected_quantity = existing_quantity + (quantity if side.upper() == "BUY" else -quantity)
        projected_exposure = current_exposure

        if existing_position is not None:
            projected_exposure -= abs(existing_quantity) * existing_position.avg_price

        projected_exposure += abs(projected_quantity) * price

        if projected_exposure > self.portfolio_risk_service.max_gross_exposure:
            return {
                "approved": False,
                "status": "REJECTED",
                "reason": (
                    "portfolio exposure exceeds limit: "
                    f"{projected_exposure} > {self.portfolio_risk_service.max_gross_exposure}"
                ),
                "order_value": quantity * price,
                "gross_exposure": projected_exposure,
            }

        portfolio.add_position(symbol, quantity if side.upper() == "BUY" else -quantity, price)
        return {
            "approved": True,
            "status": "VALIDATED",
            "reason": decision.reason,
            "order_value": quantity * price,
            "symbol": symbol,
            "side": side.upper(),
            "quantity": quantity,
        }
