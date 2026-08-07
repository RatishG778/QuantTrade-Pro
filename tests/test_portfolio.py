from core.portfolio_engine.engine import PortfolioEngine


def test_portfolio():

    engine = PortfolioEngine(

        symbols=[
            "AAPL",
            "MSFT"
        ],

        strategy_name="Moving Average",

        capital=100000

    )

    results = engine.run()

    assert len(results) == 2