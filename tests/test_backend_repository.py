from backend.app.repositories.strategy_repository import StrategyRepository


def test_strategy_repository_persists_and_lists_records():
    repo = StrategyRepository(db_path=":memory:")

    repo.save(
        {
            "id": "strategy-1",
            "name": "Momentum Strategy",
            "description": "Trend-following strategy",
            "version": "v1.0",
            "environment": "PAPER",
            "status": "draft",
        }
    )

    records = repo.list()

    assert len(records) == 1
    assert records[0]["name"] == "Momentum Strategy"
    assert records[0]["environment"] == "PAPER"
