from pathlib import Path
import pandas as pd

# -----------------------------
# Paths
# -----------------------------
RAW_PATH = Path("data/raw")
PROCESSED_PATH = Path("data/processed")

PROCESSED_PATH.mkdir(parents=True, exist_ok=True)

csv_files = list(RAW_PATH.glob("*.csv"))

print("=" * 60)
print("QuantTrade Pro - Data Cleaning")
print("=" * 60)

for file in csv_files:

    print(f"\nProcessing: {file.name}")

    df = pd.read_csv(file)

    # -----------------------------
    # Basic Information
    # -----------------------------
    print(f"Rows Before : {len(df)}")

    # Remove duplicate rows
    duplicates = df.duplicated().sum()
    df = df.drop_duplicates()

    # Remove rows with missing values
    missing = df.isnull().sum().sum()
    df = df.dropna()

    print(f"Duplicates Removed : {duplicates}")
    print(f"Missing Values     : {missing}")
    print(f"Rows After         : {len(df)}")

    # Save cleaned file
    output_file = PROCESSED_PATH / file.name
    df.to_csv(output_file, index=False)

    print("Saved:", output_file)

print("\nCleaning Completed Successfully!")