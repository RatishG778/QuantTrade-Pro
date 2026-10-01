from backend.app.services.strategy_lab import StrategyLabService


def test_strategy_lab_service_tracks_strategy_context_and_status():
    service = StrategyLabService()

    strategy = service.create_strategy(
        strategy_id="s1",
        name="Momentum Strategy",
        environment="PAPER",
        parameters={"lookback": 20},
    )

    assert strategy["status"] == "DRAFT"
    assert strategy["environment"] == "PAPER"
    assert strategy["parameters"]["lookback"] == 20

    updated = service.update_status("s1", "ACTIVE")
    assert updated["status"] == "ACTIVE"
