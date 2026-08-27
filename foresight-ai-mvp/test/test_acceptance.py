
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

def test_historical_incidents_are_used():

    response = client.post(
        "/copilot/ask",
        json={
            "question":
            "Have we seen PCF connectivity failures before?"
        }
    )

    data = response.json()

    assert response.status_code == 200

    assert len(
        data["historical_incidents"]
    ) > 0

    assert any(
        "PCF" in item["root_cause"]
        for item in data["historical_incidents"]
    )


def test_copilot_uses_historical_incidents():

    response = client.post(
        "/copilot/ask",
        json={
            "question":
            "Have we seen PCF connectivity failures before?"
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data["historical_incidents"]) > 0
    assert any(
        "PCF" in incident["root_cause"]
        for incident in data["historical_incidents"]
    )

def test_similar_incidents_retrieved():

    response = client.post(
        "/copilot/ask",
        json={
            "question": "Have we seen PCF failures before?"
        }
    )

    data = response.json()

    assert len(data["historical_incidents"]) > 0

def test_historical_incidents_in_context():

    response = client.post(
        "/copilot/ask",
        json={
            "question": "Have we seen PCF failures before?"
        }
    )

    data = response.json()

    assert "historical_incidents" in data

def test_response_uses_historical_evidence():

    response = client.post(
        "/copilot/ask",
        json={
            "question": "Have we seen PCF failures before?"
        }
    )

    data = response.json()

    assert "PCF" in data["answer"]

def test_response_contains_traceability():

    response = client.post(
        "/copilot/ask",
        json={
            "question": "Have we seen PCF failures before?"
        }
    )

    data = response.json()

    assert len(data["sources"]) > 0