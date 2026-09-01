# QuantTrade-Pro

> **Quantitative Research & Backtesting Platform**

QuantTrade-Pro is a modular Python platform engineered for quantitative strategy development, signal research, portfolio allocation analytics, Monte Carlo tail risk evaluation, machine learning baseline modeling, and interactive Streamlit visualization.

---

## 🚀 Main Features

- **Backtesting Engine**: Event-driven backtesting supporting Moving Average Crossover, RSI, and MACD strategies.
- **Risk Management**: Dynamic position sizing, configurable risk per trade, slippage, and transaction commissions.
- **Strategy Optimization**: Grid search parameter optimization, performance ranking, and heatmap visualization.
- **Walk-Forward Validation**: In-sample and out-of-sample data splitting to measure strategy robustness and prevent overfitting.
- **Monte Carlo Risk Evaluation**: Trade order permutation simulations calculating Value-at-Risk (P5, P95), win/loss probabilities, and PnL distributions.
- **Portfolio Analytics**: Multi-asset returns, annualized volatility, Sharpe ratio, max drawdown, correlation heatmaps, and allocation models.
- **Machine Learning Baseline**: Scikit-Learn Random Forest signal classifier architecture for quantitative signal filtering.
- **Structured Performance Reporting**: Machine-readable performance summaries and database persistence.
- **Streamlit Dashboard**: Professional web UI with page navigation, KPI cards, Plotly equity curves, price charts, and strategy comparisons.

---

## 📐 Platform Architecture

```text
QuantTrade-Pro/
├── app.py                     # Streamlit application entry point
├── requirements.txt           # Deployment dependencies
├── pyproject.toml             # Package configuration
├── core/
│   ├── backtesting/           # Execution engine, portfolio tracking, trade logger
│   ├── risk/                  # Position sizing, stop loss, risk management
│   ├── strategies/            # MA, RSI, MACD, Strategy Factory
│   └── feature_engineering/   # Technical indicators & features
├── research/
│   ├── database/              # SQLite experiment tracking repository
│   ├── experiments/           # Experiment runner & storage
│   ├── monte_carlo/           # Trade order randomization simulator
│   ├── optimization/          # Grid search parameter optimizer & heatmaps
│   ├── portfolio/             # Multi-asset returns, volatility, correlation & allocation
│   ├── reports/               # Performance report generator
│   └── walk_forward/          # Walk-forward validation splitters & executors
├── ml/
│   ├── models/                # BaseModel & RandomForestModel implementation
│   ├── dataset.py             # Dataset loader & preprocessor
│   └── trainer.py             # Model training pipelines
└── dashboard/                 # Streamlit UI modules (charts, metrics, sidebar, tables)
```

---

## 🛠️ Installation & Setup

### 1. Clone & Navigate
```bash
git clone https://github.com/RatishG778/QuantTrade-Pro.git
cd QuantTrade-Pro
```

### 2. Environment Setup
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

---

## 💻 Running the Platform

### Running the Streamlit Dashboard
```bash
streamlit run app.py
```

### Running the Automated Test Suite
```bash
pytest -q .\tests
```

---

## 📊 End-to-End Quantitative Workflow

```text
Market Data -> Strategy Signals -> Risk Management -> Backtesting Engine
    -> Experiment Tracking -> Parameter Optimization -> Walk-Forward Validation
    -> Monte Carlo Simulation -> Portfolio Analytics -> ML Signal Research
    -> Structured Reports -> Interactive Dashboard
```

---

## 🌐 Streamlit Cloud Deployment

This platform is configured for automated deployment on **Streamlit Cloud** via GitHub integration:
- **Repository**: `RatishG778/QuantTrade-Pro`
- **Branch**: `main`
- **Main File**: `app.py`
- **Requirements**: `requirements.txt` (Pinned UTF-8 dependencies)

---

## 🔮 Future Roadmap

- **V1.1**: Real-time market data adapters (WebSocket / REST integration)
- **V1.2**: Paper trading execution harness & simulated order book
- **V1.3**: Advanced portfolio risk constraints (CVaR, Factor Exposure)
- **V1.4**: AI Quantitative Research Assistant & LLM strategy generator
- **V1.5**: Broker API integration adapters (Interactive Brokers, Alpaca)
- **V2.0**: Production-grade live trading infrastructure

---

*QuantTrade-Pro is provided as a quantitative research and backtesting framework. Past performance simulated in backtests does not guarantee future live trading results.*
