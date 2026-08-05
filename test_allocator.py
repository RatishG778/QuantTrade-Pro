from core.portfolio_engine.allocator import PortfolioAllocator

allocator = PortfolioAllocator(100000)

allocation = allocator.equal_weight([
    "AAPL",
    "MSFT",
    "GOOGL",
    "AMZN",
    "META"
])

print("=" * 60)

for stock, info in allocation.items():

    print(stock)

    print(info)

print("=" * 60)