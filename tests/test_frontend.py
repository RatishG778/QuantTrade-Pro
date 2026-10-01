from fastapi.testclient import TestClient

from backend.app.main import app


def test_root_page_renders_frontend_shell():
    client = TestClient(app)
    response = client.get("/")

    assert response.status_code == 200
    assert "QuantTrade Pro" in response.text
    assert "Research &amp; Analytics" in response.text


def test_dashboard_page_renders_strategy_overview():
    client = TestClient(app)
    response = client.get("/dashboard")

    assert response.status_code == 200
    assert "System status" in response.text
    assert "No demo account values are shown" in response.text
    assert 'id="operations-dataset-count"' in response.text


def test_analysis_page_exposes_research_views():
    client = TestClient(app)
    response = client.get("/analysis")

    assert response.status_code == 200
    assert "Research &amp; Analytics" in response.text
    assert 'id="analysis-symbol"' in response.text
    assert 'id="refresh-market-data"' in response.text
    assert 'id="data-freshness"' in response.text
    assert 'id="strategy-comparison"' in response.text
    assert 'id="correlation-matrix"' in response.text
    assert 'id="monte-carlo-results"' in response.text
