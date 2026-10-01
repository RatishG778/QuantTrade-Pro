from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.schemas.strategy import StrategyCreateRequest


def test_health_endpoint():
    client = TestClient(app)
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_strategy_create_request_validates_required_fields():
    request = StrategyCreateRequest(
        name="Momentum Strategy",
        description="Trend-following research strategy",
        version="v1.0",
        environment="PAPER",
    )

    assert request.name == "Momentum Strategy"
    assert request.environment == "PAPER"
