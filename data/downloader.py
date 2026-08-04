from pathlib import Path
import pandas as pd
import yfinance as yf

# -----------------------------
# Paths
# -----------------------------
RAW_DATA = Path("data/raw")
RAW_DATA.mkdir(parents=True, exist_ok=True)

SYMBOL_FILE = Path("data/symbols/symbols.csv")

# -----------------------------
# Read symbols
# -----------------------------
symbols = pd.read_csv(SYMBOL_FILE)["Symbol"].tolist()

print("=" * 50)
print("QuantTrade Pro Data Downloader")
print("=" * 50)

for symbol in symbols:

    print(f"\nDownloading {symbol}...")

    try:

        df = yf.download(
           symbol,
           period="5y",
           interval="1d",
           auto_adjust=True,
           progress=False,
           group_by="column",
           multi_level_index=False
        )

        if df.empty:
            print(f"No data for {symbol}")
            continue

        file_path = RAW_DATA / f"{symbol}.csv"

        df.to_csv(file_path)

        print(f"Saved -> {file_path}")

    except Exception as e:

        print(f"Error downloading {symbol}")
        print(e)

print("\nDownload Complete.")