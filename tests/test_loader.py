from core.portfolio_engine.loader import PortfolioLoader


def test_loader():

    loader = PortfolioLoader()

    portfolio = loader.load([
        "AAPL",
        "MSFT"
    ])

    assert len(portfolio) == 2

    assert "AAPL" in portfolio

    assert "MSFT" in portfolio