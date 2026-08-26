from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_endpoint_contract():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "running", "service": "foresight-ai-mvp"}


def test_scenario_list_contract_contains_required_fields():
    response = client.get("/scenario/list")
    assert response.status_code == 200
    payload = response.json()
    assert "scenarios" in payload
    assert payload["scenarios"][0]["name"]
    assert payload["scenarios"][0]["description"]
    assert payload["scenarios"][0]["affected_nodes"]


def test_foresight_contract_exposes_network_status_and_anomalies():
    response = client.get("/kpi/foresight")
    assert response.status_code == 200
    payload = response.json()
    assert "network_status" in payload
    assert "anomalies" in payload
    assert isinstance(payload["anomalies"], dict)
