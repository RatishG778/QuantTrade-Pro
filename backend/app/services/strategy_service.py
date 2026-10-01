from __future__ import annotations

from uuid import uuid4

from backend.app.schemas.strategy import StrategyCreateRequest, StrategyResponse


class StrategyService:
    def create_strategy(self, request: StrategyCreateRequest) -> StrategyResponse:
        return StrategyResponse(
            id=str(uuid4()),
            name=request.name,
            description=request.description,
            version=request.version,
            environment=request.environment,
            status="draft",
        )
