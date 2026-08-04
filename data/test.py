import pandas as pd

df = pd.read_csv("data/processed/AAPL.csv")

print(df.head())
print("\n")
print(df.columns)
print("\n")
print(df.dtypes)
