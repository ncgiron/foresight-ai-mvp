from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_scenario_change_refreshes_dashboard_health_payload():
    client.post("/scenario/set", json={"scenario": "smf_overload"})

    response = client.get("/kpi/foresight")
    assert response.status_code == 200
    payload = response.json()
    assert payload["network_status"] in {"healthy", "root_cause_identified", "anomaly_detected"}

    client.post("/scenario/set", json={"scenario": None})
