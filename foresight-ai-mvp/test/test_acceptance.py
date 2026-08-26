from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_scenario_activation_updates_timeseries_and_current_selection():
    response = client.post("/scenario/set", json={"scenario": "upf_congestion"})
    assert response.status_code == 200
    assert response.json()["scenario"] == "upf_congestion"

    current = client.get("/scenario/current")
    assert current.status_code == 200
    assert current.json()["scenario"] == "upf_congestion"

    timeseries = client.get("/kpi/timeseries?minutes=5&days=1")
    payload = timeseries.json()
    assert payload["timeseries"]["UPF"][-1]["cpu_usage"] == 95
    assert payload["timeseries"]["UPF"][-1]["latency_ms"] == 120

    cleared = client.post("/scenario/set", json={"scenario": None})
    assert cleared.status_code == 200
    assert cleared.json()["scenario"] is None
