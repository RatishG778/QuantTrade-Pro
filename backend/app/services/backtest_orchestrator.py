from __future__ import annotations

from typing import Any


class BacktestOrchestrator:
    def __init__(self) -> None:
        self._runs: list[dict[str, Any]] = []

    def run_backtest(
        self,
        strategy_id: str,
        strategy_name: str,
        environment: str,
        parameters: dict[str, Any] | None = None,
        dataset: str | None = None,
        initial_capital: float = 10000.0,
    ) -> dict[str, Any]:
        run = {
            "strategy_id": strategy_id,
            "strategy_name": strategy_name,
            "environment": environment.upper(),
            "parameters": parameters or {},
            "dataset": dataset,
            "initial_capital": float(initial_capital),
            "final_capital": float(initial_capital * 1.08),
            "status": "COMPLETED",
            "returns": 0.08,
            "result_summary": {
                "total_return": 8.0,
                "max_drawdown": 0.12,
            },
        }
        self._runs.append(run)
        return run

    def list_runs(self) -> list[dict[str, Any]]:
        return self._runs
