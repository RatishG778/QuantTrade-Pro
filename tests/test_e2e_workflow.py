import pytest
import pandas as pd
import numpy as np

from core.strategies.strategy_factory import StrategyFactory
from core.backtesting.engine import BacktestEngine
from research.optimization.optimizer import Optimizer
from research.monte_carlo.simulator import MonteCarloSimulator
from research.portfolio.analytics import PortfolioAnalytics
from ml.models.random_forest import RandomForestModel
from research.reports.performance_report import PerformanceReport
from research.database.repository import ExperimentRepository


def test_end_to_end_quant_workflow():
    # 1. Deterministic Market Data
    dates = pd.date_range("2024-01-01", periods=100)
    np.random.seed(42)
    prices = 100 + np.cumsum(np.random.randn(100))
    df = pd.DataFrame({
        "Open": prices,
        "High": prices + 1,
        "Low": prices - 1,
        "Close": prices,
        "Volume": 1000
    }, index=dates)

    # 2. Strategy instantiation via factory
    strategy = StrategyFactory.get_strategy("Moving Average", df, fast=5, slow=20)
    assert strategy is not None

    # 3. Backtesting
    engine = BacktestEngine(strategy, initial_capital=10000.0)
    result = engine.run()
    assert result is not None
    assert hasattr(result, "profit")

    # 4. Experiment Tracking / DB Save
    repo = ExperimentRepository()
    exp_data = {
        "created_at": "2026-09-01 00:00:00",
        "strategy": "Moving Average",
        "symbol": "TEST",
        "capital": 10000.0,
        "parameters": "{'fast': 5, 'slow': 20}",
        "profit": float(result.profit),
        "return_pct": 5.0,
        "sharpe": 1.2,
        "max_drawdown": -0.05,
        "trades": len(result.trades) if isinstance(result.trades, list) else int(result.trades),
        "win_rate": 0.6
    }
    repo.save(exp_data)
    history = repo.get_all()
    assert len(history) > 0

    # 5. Optimization
    optimizer = Optimizer()
    assert optimizer is not None

    # 6. Monte Carlo
    mc_sim = MonteCarloSimulator()
    mc_results = mc_sim.simulate([10.0, -5.0, 15.0, -2.0], simulations=10)
    assert len(mc_results) == 10

    # 7. Portfolio Analytics
    series_rets = pd.Series([0.01, -0.005, 0.02, 0.003])
    ann_ret = PortfolioAnalytics.annualized_return(series_rets)
    ann_vol = PortfolioAnalytics.annualized_volatility(series_rets)
    sharpe = PortfolioAnalytics.sharpe_ratio(series_rets)
    mdd = PortfolioAnalytics.max_drawdown(series_rets)
    assert isinstance(ann_ret, float)
    assert isinstance(ann_vol, float)
    assert isinstance(sharpe, float)
    assert isinstance(mdd, float)

    # 8. ML Baseline
    ml_model = RandomForestModel()
    X = np.random.randn(50, 4)
    y = np.random.randint(0, 2, 50)
    ml_model.train(X, y)
    preds = ml_model.predict(X)
    acc = ml_model.evaluate(X, y)
    assert len(preds) == 50
    assert 0.0 <= acc <= 1.0

    # 9. Performance Report
    report = PerformanceReport().generate(result)
    assert report is not None
    assert "summary" in report
    assert "risk" in report
    assert "trade_analysis" in report
