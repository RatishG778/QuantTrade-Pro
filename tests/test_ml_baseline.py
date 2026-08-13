import pandas as pd

from ml.features import FeatureEngineer
from ml.trainer import MLTrainer
from ml.evaluator import MLEvaluator


def test_ml_pipeline():

    data = pd.DataFrame({
        "Close": [
            100, 101, 102, 101, 103,
            105, 104, 106, 108, 107,
            109, 111, 110, 112, 114,
            113, 115, 117, 116, 118,
            120, 119, 121, 123, 122
        ]
    })

    features = FeatureEngineer().transform(data)

    feature_columns = [
        "return_1",
        "return_5",
        "ma_5",
        "ma_20",
        "ma_ratio"
    ]

    X = features[feature_columns]
    y = features["target"]

    model = MLTrainer()

    model.train(X, y)

    predictions = model.predict(X)

    metrics = MLEvaluator().evaluate(
        y,
        predictions
    )

    assert len(predictions) == len(y)

    assert 0 <= metrics["accuracy"] <= 1

    assert 0 <= metrics["precision"] <= 1

    assert 0 <= metrics["recall"] <= 1

    assert 0 <= metrics["f1"] <= 1