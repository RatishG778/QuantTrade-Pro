from __future__ import annotations

from dataclasses import dataclass
import os


@dataclass
class EnvironmentConfig:
    environment: str = "DEVELOPMENT"
    live_enabled: bool = False
    paper_enabled: bool = True
    readiness_check: bool = False

    def __post_init__(self) -> None:
        if self.environment == "LIVE" and not self.live_enabled:
            self.live_enabled = False


def get_environment_config(
    environment: str | None = None,
    live_enabled: bool | None = None,
    paper_enabled: bool | None = None,
    readiness_check: bool | None = None,
) -> EnvironmentConfig:
    env = environment or os.getenv("QUANTTRADE_ENV", "DEVELOPMENT")
    live = live_enabled if live_enabled is not None else os.getenv("QUANTTRADE_LIVE_ENABLED", "false").lower() == "true"
    paper = paper_enabled if paper_enabled is not None else os.getenv("QUANTTRADE_PAPER_ENABLED", "true").lower() == "true"
    readiness = readiness_check if readiness_check is not None else os.getenv("QUANTTRADE_READINESS_CHECK", "false").lower() == "true"
    return EnvironmentConfig(
        environment=env.upper(),
        live_enabled=live,
        paper_enabled=paper,
        readiness_check=readiness,
    )
