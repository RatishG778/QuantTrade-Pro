from core.portfolio_engine.loader import PortfolioLoader

loader = PortfolioLoader()

portfolio = loader.load([
    "AAPL",
    "MSFT",
    "GOOGL",
    "AMZN",
    "META"
])

print("=" * 50)

for symbol, df in portfolio.items():

    print(symbol)

    print(df.shape)

print("=" * 50)