import pandas as pd

from research.walk_forward.splitter import WalkForwardSplitter

df = pd.read_csv("data/features/AAPL.csv")

splitter = WalkForwardSplitter()

train, test = splitter.split(df)

print("=" * 60)

print("Training Rows :", len(train))

print("Testing Rows  :", len(test))

print("=" * 60)