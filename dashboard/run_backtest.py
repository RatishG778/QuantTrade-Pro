from pathlib import Path

import pandas as pd

from core.backtesting.engine import BacktestEngine
from core.strategies.strategy_factory import StrategyFactory

from config.settings import (
    INITIAL_CAPITAL,
    DEFAULT_STRATEGY,
    DEFAULT_SYMBOL,
)

from core.exceptions import QuantTradeError
from config.logger import logger


BASE_DIR = Path(__file__).resolve().parent.parent


def run_backtest(
    symbol=DEFAULT_SYMBOL,
    capital=INITIAL_CAPITAL,
    strategy_name=DEFAULT_STRATEGY,
):

    try:

        file_path = (
            BASE_DIR
            / "data"
            / "features"
            / f"{symbol}.csv"
        )

        df = pd.read_csv(file_path)

        strategy = StrategyFactory.get_strategy(
            strategy_name,
            df
        )

        engine = BacktestEngine(
            strategy,
            initial_capital=capital
        )

        return engine.run()

    except QuantTradeError as e:

        logger.error(str(e))
        raise

    except Exception as e:

        logger.exception(e)
        raise


def compare_strategies(symbol, capital):

    strategies = [

        "Moving Average",

        "RSI",

        "MACD"

    ]

    results = []

    for strategy_name in strategies:

        result = run_backtest(

            symbol,

            capital,

            strategy_name

        )

        results.append({

            "Strategy": strategy_name,

            "Profit": result.profit,

            "Trades": result.trades,

            "Final Capital": result.final_capital

        })

    return results