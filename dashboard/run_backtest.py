from pathlib import Path
import pandas as pd
from core.backtesting.engine import BacktestEngine
from core.strategies.strategy_factory import StrategyFactory


def run_backtest(symbol, capital,strategy_name):

    BASE_DIR = Path(__file__).resolve().parent.parent

    df = pd.read_csv(
        BASE_DIR / "data" / "features" / f"{symbol}.csv"
    )

    strategy = StrategyFactory.get_strategy(
        strategy_name,
        df
    )

    data = strategy.generate_signals()

    print(data.columns.tolist())

    engine = BacktestEngine(
        strategy,
        initial_capital=capital
    )

    engine.run()

    return {
        "capital": engine.portfolio.cash,
        "profit": sum(engine.portfolio.trade_history),
        "trades": len(engine.portfolio.trade_history),
        "equity_curve": engine.portfolio.equity_curve,
        "trade_history": engine.portfolio.trade_history,
        "data": data
    }
def compare_strategies(symbol, capital):

    strategies = [
        "Moving Average",
        "RSI",
        "MACD"
    ]

    summary = []

    for name in strategies:

        result = run_backtest(
            symbol,
            capital,
            name
        )

        summary.append({

            "Strategy": name,

            "Return (%)":
            round(
                result["profit"] /
                capital * 100,
                2
            ),

            "Trades":
            result["trades"],

            "Profit":
            round(
                result["profit"],
                2
            )
        })

    return summary