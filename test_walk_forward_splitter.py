import pandas as pd

from research.validation.splitter import WalkForwardSplitter

df = pd.read_csv(

    "data/features/AAPL.csv"

)

splitter = WalkForwardSplitter()

windows = splitter.split(df)

print("=" * 60)

print("Windows:", len(windows))

print("=" * 60)

for i, (train, test) in enumerate(

    windows[:3],

    start=1

):

    print(

        f"Window {i}"

    )

    print(

        len(train),

        len(test)

    )