from core.backtesting.engine import BacktestEngine
from core.strategies.strategy_factory import StrategyFactory


class WalkForwardExecutor:

    def execute(

        self,

        windows,

        strategy_name,

        parameters=None,

        capital=100000

    ):

        if parameters is None:
            parameters = {}

        results = []

        for train, test in windows:

            strategy = StrategyFactory.get_strategy(

                strategy_name,

                test,

                **parameters

            )

            engine = BacktestEngine(

                strategy,

                initial_capital=capital

            )

            result = engine.run()

            results.append(result)

        return results