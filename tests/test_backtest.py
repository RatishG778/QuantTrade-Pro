import pandas as pd

from core.strategies.moving_average import MovingAverageStrategy
from core.backtesting.engine import BacktestEngine


df = pd.read_csv(
    "feature_engineering/output/AAPL.csv"
)

strategy = MovingAverageStrategy(df)

engine = BacktestEngine(strategy)

results = engine.run()