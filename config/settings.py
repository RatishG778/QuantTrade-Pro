from pathlib import Path


# --------------------------------------
# Project
# --------------------------------------

PROJECT_NAME = "QuantTrade-Pro"

VERSION = "5.0"

# --------------------------------------
# Paths
# --------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"

RAW_DATA = DATA_DIR / "raw"

PROCESSED_DATA = DATA_DIR / "processed"

FEATURE_DATA = DATA_DIR / "features"

REPORT_DIR = BASE_DIR / "research" / "reports"

LOG_DIR = BASE_DIR / "logs"

# --------------------------------------
# Trading
# --------------------------------------

INITIAL_CAPITAL = 100000

RISK_PER_TRADE = 0.02

COMMISSION = 0.001

SLIPPAGE = 0.0005

# --------------------------------------
# Dashboard
# --------------------------------------

DEFAULT_SYMBOL = "AAPL"

DEFAULT_STRATEGY = "Moving Average"