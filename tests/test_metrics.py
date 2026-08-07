from core.portfolio_engine.metrics import PortfolioMetrics


def test_metrics():

    sample = {

        "AAPL": {
            "Profit": 1000,
            "Trades": 5,
            "Final Capital": 101000
        },

        "MSFT": {
            "Profit": -500,
            "Trades": 3,
            "Final Capital": 99500
        }

    }

    metrics = PortfolioMetrics(sample)

    summary = metrics.calculate()

    assert summary["Portfolio Profit"] == 500

    assert summary["Total Trades"] == 8