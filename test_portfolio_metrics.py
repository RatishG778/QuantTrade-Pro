from core.portfolio_engine.engine import PortfolioEngine
from core.portfolio_engine.metrics import PortfolioMetrics

engine = PortfolioEngine(
    symbols=[
        "AAPL",
        "MSFT",
        "GOOGL",
        "AMZN",
        "META"
    ],
    strategy_name="Moving Average",
    capital=100000
)

results = engine.run()

metrics = PortfolioMetrics(results)

summary = metrics.calculate()

print("=" * 60)

for key, value in summary.items():

    print(f"{key:20}: {value}")

print("=" * 60)