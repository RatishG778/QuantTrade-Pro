from core.strategies.moving_average import MovingAverageStrategy
from core.strategies.rsi_strategy import RSIStrategy
from core.strategies.macd_strategy import MACDStrategy

from core.exceptions import StrategyError


class StrategyFactory:

    @staticmethod
    def get_strategy(
        name,
        data,
        **kwargs
    ):

        if name == "Moving Average":

            return MovingAverageStrategy(

                data,

                fast=kwargs.get("fast", 20),

                slow=kwargs.get("slow", 50)

            )

        elif name == "RSI":

            return RSIStrategy(data)

        elif name == "MACD":

            return MACDStrategy(data)

        raise StrategyError(
            f"Unknown strategy: {name}"
        )