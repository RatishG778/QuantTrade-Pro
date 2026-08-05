from core.portfolio_engine.loader import PortfolioLoader
from core.exceptions import QuantTradeError

loader = PortfolioLoader()

try:
    loader.load(["INVALID_STOCK"])

except QuantTradeError as e:
    print("=" * 60)
    print("QuantTrade-Pro Error")
    print("=" * 60)
    print(e)