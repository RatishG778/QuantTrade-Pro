from __future__ import annotations

from typing import Any


class PortfolioRiskService:
    def __init__(self, max_gross_exposure: float = 5000.0) -> None:
        self.max_gross_exposure = max_gross_exposure

    def evaluate_portfolio(
        self,
        cash: float,
        positions: dict[str, int],
        prices: dict[str, float],
    ) -> dict[str, Any]:
        gross_exposure = 0.0
        for symbol, quantity in positions.items():
            gross_exposure += abs(quantity) * prices.get(symbol, 0.0)

        if gross_exposure > self.max_gross_exposure:
            risk_status = "CRITICAL"
            blocked = True
        elif gross_exposure > self.max_gross_exposure * 0.75:
            risk_status = "WARN"
            blocked = False
        else:
            risk_status = "OK"
            blocked = False

        return {
            "cash": float(cash),
            "position_count": len(positions),
            "gross_exposure": gross_exposure,
            "risk_status": risk_status,
            "blocked": blocked,
            "max_gross_exposure": self.max_gross_exposure,
        }
