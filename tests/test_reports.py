import pandas as pd

from core.backtesting.result import BacktestResult
from research.reports.performance_report import PerformanceReport


def test_performance_report():

    result = BacktestResult(
        data=pd.DataFrame(),
        profit=1500.0,
        trades=10,
        trade_history=[100, 200, -50],
        equity=[100000, 101500],
        final_capital=101500,
        average_win=150.0,
        average_loss=-50.0,
        profit_factor=3.0,
        risk_reward=3.0,
        max_drawdown=-0.05,
    )

    report = PerformanceReport().generate(result)

    assert report["summary"]["profit"] == 1500.0
    assert report["summary"]["trades"] == 10
    assert report["summary"]["final_capital"] == 101500

    assert report["risk"]["max_drawdown"] == -0.05
    assert report["risk"]["profit_factor"] == 3.0