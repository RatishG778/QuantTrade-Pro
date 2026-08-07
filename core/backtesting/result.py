from dataclasses import dataclass
import pandas as pd


@dataclass
class BacktestResult:

    data: pd.DataFrame

    profit: float

    trades: int

    trade_history: list

    equity: list

    final_capital: float

    average_win: float

    average_loss: float

    profit_factor: float

    risk_reward: float

    max_drawdown: float