from dataclasses import asdict
from typing import Any

from core.backtesting.result import BacktestResult


class PerformanceReport:

    def generate(
        self,
        result: BacktestResult
    ) -> dict[str, Any]:

        return {
            "summary": {
                "profit": result.profit,
                "return_pct": result.return_pct,
                "trades": result.trades,
                "win_rate": result.win_rate,
                "final_capital": result.final_capital,
            },
            "risk": {
                "max_drawdown": result.max_drawdown,
                "profit_factor": result.profit_factor,
                "risk_reward": result.risk_reward,
            },
            "trade_analysis": {
                "average_win": result.average_win,
                "average_loss": result.average_loss,
            },
        }