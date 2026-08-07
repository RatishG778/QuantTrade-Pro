from core.portfolio_engine.loader import PortfolioLoader

loader = PortfolioLoader()

portfolio = loader.load(

    [

        "AAPL",

        "MSFT",

        "GOOGL",

        "META",

        "NVDA"

    ]

)

print("=" * 60)

print("Loaded Stocks")

print("=" * 60)

for symbol in portfolio:

    print(symbol, len(portfolio[symbol]))
    