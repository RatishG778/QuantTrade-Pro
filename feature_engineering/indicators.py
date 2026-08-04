from pathlib import Path
import pandas as pd
import ta

# ----------------------------------
# Paths
# ----------------------------------

INPUT_PATH = Path("data/processed")
OUTPUT_PATH = Path("feature_engineering/output")

OUTPUT_PATH.mkdir(parents=True, exist_ok=True)

files = list(INPUT_PATH.glob("*.csv"))

print("=" * 60)
print("QuantTrade Pro - Feature Engineering")
print("=" * 60)

for file in files:

    print(f"\nProcessing {file.name}")

    df = pd.read_csv(file)

    # -------------------------------
    # Moving Averages
    # -------------------------------

    df["SMA_20"] = ta.trend.sma_indicator(df["Close"], window=20)
    df["SMA_50"] = ta.trend.sma_indicator(df["Close"], window=50)

    df["EMA_20"] = ta.trend.ema_indicator(df["Close"], window=20)

    # -------------------------------
    # RSI
    # -------------------------------

    df["RSI"] = ta.momentum.rsi(df["Close"], window=14)

    # -------------------------------
    # MACD
    # -------------------------------

    df["MACD"] = ta.trend.macd(df["Close"])

    df["MACD_SIGNAL"] = ta.trend.macd_signal(df["Close"])

    # -------------------------------
    # Bollinger Bands
    # -------------------------------

    df["BB_UPPER"] = ta.volatility.bollinger_hband(df["Close"])

    df["BB_LOWER"] = ta.volatility.bollinger_lband(df["Close"])

    # -------------------------------
    # ATR
    # -------------------------------

    df["ATR"] = ta.volatility.average_true_range(
        df["High"],
        df["Low"],
        df["Close"]
    )

    # -------------------------------
    # Returns
    # -------------------------------

    df["Daily_Return"] = df["Close"].pct_change()

    df["Log_Return"] = (
        (df["Close"] / df["Close"].shift(1))
    ).apply(lambda x: pd.NA if pd.isna(x) else __import__("numpy").log(x))

    # -------------------------------
    # Volatility
    # -------------------------------

    df["Volatility"] = df["Daily_Return"].rolling(20).std()

    output_file = OUTPUT_PATH / file.name

    df.to_csv(output_file, index=False)

    print(f"Saved -> {output_file}")

print("\nFeature Engineering Completed Successfully!")