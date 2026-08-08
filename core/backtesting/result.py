from dataclasses import dataclass
from typing import Any

import pandas as pd


@dataclass
class BacktestResult:

    data: pd.DataFrame

    profit: float

    trades: int

    trade_history: list[Any]

    equity: list[Any]

    final_capital: float

    average_win: float

    average_loss: float

    profit_factor: float

    risk_reward: float

    max_drawdown: float

    @property
    def return_pct(self) -> float:
        """Return percentage based on initial and final capital."""

        if not self.equity:
            return 0.0

        initial_capital = self.equity[0]

        if initial_capital == 0:
            return 0.0

        return (
            (self.final_capital - initial_capital)
            / initial_capital
            * 100
        )

    @property
    def win_rate(self) -> float:
        """Percentage of profitable trades."""

        if not self.trade_history:
            return 0.0

        winning_trades = sum(
            1
            for trade in self.trade_history
            if trade > 0
        )

        return (
            winning_trades
            / len(self.trade_history)
            * 100
        )