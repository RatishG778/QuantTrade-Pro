import pandas as pd

from strategies.moving_average import MovingAverageStrategy


df = pd.read_csv(
    "feature_engineering/output/AAPL.csv"
)

strategy = MovingAverageStrategy(df)

result = strategy.generate_signals()

print(result[["Close", "SMA_20", "SMA_50", "Signal"]].tail())