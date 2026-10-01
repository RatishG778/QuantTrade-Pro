from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


Environment = Literal["DEVELOPMENT", "PAPER", "LIVE"]


class StrategyCreateRequest(BaseModel):
    name: str = Field(..., min_length=1, description="Strategy name")
    description: str = Field(default="", description="Human-readable strategy summary")
    version: str = Field(default="v1.0", description="Strategy version")
    environment: Environment = Field(default="PAPER", description="Execution environment")


class StrategyResponse(BaseModel):
    id: str
    name: str
    description: str
    version: str
    environment: Environment
    status: str = "draft"
