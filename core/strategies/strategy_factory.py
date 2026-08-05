from core.strategies.moving_average import MovingAverageStrategy
from core.strategies.rsi_strategy import RSIStrategy
from core.strategies.macd_strategy import MACDStrategy
from core.exceptions import StrategyError


class StrategyFactory:

    @staticmethod
    def get_strategy(name, data):

        strategies = {
            "Moving Average": MovingAverageStrategy,
            "RSI": RSIStrategy,
            "MACD": MACDStrategy,
        }

        if name not in strategies:
            raise StrategyError(f"Unknown strategy: {name}")

        return strategies[name](data)