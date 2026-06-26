from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "running"


def test_smf_analysis_endpoint():
    response = client.get("/kpi/smf/analysis")
    assert response.status_code == 200
    payload = response.json()
    assert payload["node"] == "SMF01"
    assert payload["analysis"]["risk_level"] in {"LOW", "MEDIUM", "HIGH"}
    assert payload["analysis"]["health_score"] >= 0
