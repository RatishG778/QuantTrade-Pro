from core.portfolio_engine.engine import PortfolioEngine

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

print("=" * 60)

for stock, result in results.items():

    print(stock)

    print(result)

    print()

print("=" * 60)