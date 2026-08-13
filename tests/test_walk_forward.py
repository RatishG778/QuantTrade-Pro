import pandas as pd

from research.validation.walk_forward import WalkForwardValidator


def test_walk_forward_creates_windows():

    data = pd.DataFrame({
        "Close": range(1, 101)
    })

    validator = WalkForwardValidator(
        train_size=60,
        test_size=20,
        step_size=20
    )

    windows = list(validator.split(data))

    assert len(windows) == 2

    train_1, test_1 = windows[0]

    assert len(train_1) == 60
    assert len(test_1) == 20

    train_2, test_2 = windows[1]

    assert len(train_2) == 60
    assert len(test_2) == 20

    assert train_1.iloc[-1]["Close"] == 60
    assert test_1.iloc[0]["Close"] == 61

    assert train_2.iloc[0]["Close"] == 21
    assert test_2.iloc[0]["Close"] == 81


def test_walk_forward_run():

    data = pd.DataFrame({
        "Close": range(1, 101)
    })

    validator = WalkForwardValidator(
        train_size=60,
        test_size=20,
        step_size=20
    )

    def evaluator(train_data, test_data):

        return {
            "profit": float(
                test_data["Close"].iloc[-1]
                - test_data["Close"].iloc[0]
            ),
            "return_pct": 10.0
        }

    result = validator.run(
        data,
        evaluator
    )

    assert len(result.results) == 2
    assert result.total_profit == 38.0
    assert result.average_return == 10.0