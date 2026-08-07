from core.strategies.moving_average import MovingAverageStrategy


def test_strategy(sample_data):

    strategy = MovingAverageStrategy(
        sample_data
    )

    result = strategy.generate_signals()

    assert "Signal" in result.columns