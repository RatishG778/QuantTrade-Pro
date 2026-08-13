import pandas as pd

from ml.dataset_builder import DatasetBuilder

df = pd.read_csv("data/features/AAPL.csv")

df["Target"] = (
    df["Close"].shift(-1) > df["Close"]
).astype(int)

builder = DatasetBuilder(df)

X_train, X_test, y_train, y_test = builder.classification_dataset(
    features=[
        "RSI",
        "MACD",
        "SMA_20",
        "SMA_50",
        "Volume"
    ]
)

print("Training:", X_train.shape)
print("Testing :", X_test.shape)