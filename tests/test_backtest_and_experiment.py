from backend.app.services.backtest_orchestrator import BacktestOrchestrator


def test_backtest_orchestrator_records_reproducible_run():
    orchestrator = BacktestOrchestrator()

    run = orchestrator.run_backtest(
        strategy_id="s1",
        strategy_name="Momentum Strategy",
        environment="PAPER",
        parameters={"lookback": 20},
        dataset="sample_data.csv",
        initial_capital=10000,
    )

    assert run["strategy_id"] == "s1"
    assert run["environment"] == "PAPER"
    assert run["parameters"]["lookback"] == 20
    assert run["status"] == "COMPLETED"
    assert run["final_capital"] > 0
    assert len(orchestrator.list_runs()) >= 1
