from core.portfolio_engine.loader import PortfolioLoader
from core.strategies.strategy_factory import StrategyFactory
from core.backtesting.engine import BacktestEngine
from core.portfolio_engine.allocator import PortfolioAllocator

class PortfolioEngine:

    def __init__(self, symbols, strategy_name, capital):

        self.symbols = symbols
        self.strategy_name = strategy_name
        self.capital = capital

        self.loader = PortfolioLoader()

    def run(self):

        portfolio = self.loader.load(self.symbols)

        results = {}

        allocator = PortfolioAllocator(self.capital)
        allocation = allocator.equal_weight(
            list(portfolio.keys())
        )

        for symbol, df in portfolio.items():

            strategy = StrategyFactory.get_strategy(
                self.strategy_name,
                df
            )

            engine = BacktestEngine(
                strategy,
                initial_capital=allocation[symbol]["capital"]
            )

            engine.run()

            results[symbol] = {
                "Final Capital": engine.portfolio.cash,
                "Profit": sum(engine.portfolio.trade_history),
                "Trades": len(engine.portfolio.trade_history)
            }

        return results