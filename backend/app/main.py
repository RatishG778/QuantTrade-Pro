from __future__ import annotations

from pathlib import Path
from typing import Literal

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from backend.app.schemas.strategy import StrategyCreateRequest, StrategyResponse
from backend.app.services.analytics_service import ResearchAnalyticsService
from backend.app.services.market_data_service import MarketDataService
from backend.app.services.strategy_service import StrategyService

APP_ROOT = Path(__file__).resolve().parent.parent.parent
FRONTEND_DIR = APP_ROOT / "frontend"

app = FastAPI(
    title="QuantTrade Pro",
    version="0.1.0",
    description="Production-grade quantitative trading platform with a modern web frontend.",
)

app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR / "static")), name="static")
templates = Jinja2Templates(directory=str(FRONTEND_DIR / "templates"))
analytics_service = ResearchAnalyticsService()
market_data_service = MarketDataService()


class MarketDataRefreshRequest(BaseModel):
    symbol: str = Field(min_length=1, max_length=12)
    period: Literal["1y", "2y", "5y"] = "5y"


@app.get("/", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    rendered = templates.get_template("index.html").render(
        request=request,
        title="QuantTrade Pro | Overview",
    )
    return HTMLResponse(rendered)


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request) -> HTMLResponse:
    rendered = templates.get_template("dashboard.html").render(
        request=request,
        title="QuantTrade Pro | Dashboard",
    )
    return HTMLResponse(rendered)


@app.get("/analysis", response_class=HTMLResponse)
async def analysis(request: Request) -> HTMLResponse:
    rendered = templates.get_template("analysis.html").render(
        request=request,
        title="QuantTrade Pro | Research & Analytics",
    )
    return HTMLResponse(rendered)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "quanttrade-pro"}


@app.get("/api/v1/overview")
def overview() -> dict[str, object]:
    return {
        "data_status": "NOT_CONNECTED",
        "portfolio": {
            "net_equity": None,
            "daily_pnl": None,
            "drawdown": None,
            "open_positions": None,
        },
        "performance": None,
        "risk": {
            "status": "UNAVAILABLE",
            "blocked": True,
            "max_gross_exposure": None,
            "current_exposure": None,
        },
        "environment": {
            "mode": "PAPER",
            "live_allowed": False,
        },
        "strategies": [],
    }


@app.get("/api/v1/strategies")
def list_strategies() -> list[StrategyResponse]:
    return []


@app.get("/api/v1/analysis/catalog")
def analysis_catalog() -> dict[str, object]:
    return analytics_service.catalog()


@app.get("/api/v1/market-data/status")
def market_data_status() -> dict[str, object]:
    return market_data_service.status()


@app.post("/api/v1/market-data/refresh")
def refresh_market_data(request: MarketDataRefreshRequest) -> dict[str, object]:
    try:
        return market_data_service.refresh(request.symbol, request.period)
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error
    except RuntimeError as error:
        raise HTTPException(status_code=502, detail=str(error)) from error


@app.get("/api/v1/analysis/report")
def analysis_report(
    symbol: str = Query(min_length=1, max_length=12),
    strategy: str = Query(default="Moving Average"),
) -> dict[str, object]:
    try:
        return analytics_service.report(symbol=symbol, selected_strategy=strategy)
    except KeyError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error


@app.post("/api/v1/strategies", response_model=StrategyResponse)
def create_strategy(request: StrategyCreateRequest) -> StrategyResponse:
    return StrategyService().create_strategy(request)
