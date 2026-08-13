from research.monte_carlo.simulator import MonteCarloSimulator
from research.monte_carlo.report import MonteCarloReport


def test_monte_carlo_pipeline():

    trades = [
        100,
        -50,
        200,
        -100,
        150
    ]

    results = MonteCarloSimulator().simulate(
        trades,
        simulations=100
    )

    assert len(results) == 100

    report = MonteCarloReport().generate(
        results
    )

    assert "best" in report
    assert "worst" in report
    assert "average" in report
    assert "median" in report
    assert "p5" in report
    assert "p95" in report
    assert "probability_of_profit" in report
    assert "probability_of_loss" in report