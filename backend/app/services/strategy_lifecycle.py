from __future__ import annotations

from backend.app.config import EnvironmentConfig


class StrategyLifecycleService:
    def __init__(self, config: EnvironmentConfig | None = None) -> None:
        self.config = config or EnvironmentConfig()

    def activate_strategy(self, strategy_id: str, environment: str) -> dict[str, object]:
        env_name = environment.upper()

        if env_name == "LIVE":
            if not self.config.live_enabled or not self.config.readiness_check:
                return {
                    "approved": False,
                    "status": "BLOCKED",
                    "reason": "LIVE activation blocked: readiness checks are not complete.",
                    "strategy_id": strategy_id,
                    "environment": env_name,
                }

        if env_name not in {"DEVELOPMENT", "PAPER", "LIVE"}:
            return {
                "approved": False,
                "status": "BLOCKED",
                "reason": "Unsupported environment.",
                "strategy_id": strategy_id,
                "environment": env_name,
            }

        return {
            "approved": True,
            "status": "ACTIVE",
            "reason": "activation approved",
            "strategy_id": strategy_id,
            "environment": env_name,
        }
