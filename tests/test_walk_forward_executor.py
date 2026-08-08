import pandas as pd

from research.validation.splitter import WalkForwardSplitter
from research.validation.executor import WalkForwardExecutor

df = pd.read_csv("data/features/AAPL.csv")

splitter = WalkForwardSplitter()

windows = splitter.split(df)

executor = WalkForwardExecutor()

results = executor.execute(

    windows,

    "Moving Average",

    {

        "fast":10,

        "slow":60

    }

)

print("="*60)

print("Completed Windows:", len(results))

print("="*60)

for i, result in enumerate(results[:3], start=1):

    print(

        i,

        result.profit,

        result.trades

    )