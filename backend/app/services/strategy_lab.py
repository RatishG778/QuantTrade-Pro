from __future__ import annotations

from typing import Any


class StrategyLabService:
    def __init__(self) -> None:
        self._strategies: dict[str, dict[str, Any]] = {}

    def create_strategy(
        self,
        strategy_id: str,
        name: str,
        environment: str,
        parameters: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        strategy = {
            "id": strategy_id,
            "name": name,
            "environment": environment.upper(),
            "status": "DRAFT",
            "parameters": parameters or {},
            "dataset": None,
            "backtest_results": None,
            "validation_results": None,
            "deployment_status": "NOT_DEPLOYED",
        }
        self._strategies[strategy_id] = strategy
        return strategy

    def update_status(self, strategy_id: str, status: str) -> dict[str, Any]:
        strategy = self._strategies[strategy_id]
        strategy["status"] = status.upper()
        return strategy

    def get_strategy(self, strategy_id: str) -> dict[str, Any]:
        return self._strategies[strategy_id]
