import requests
from fastapi.testclient import TestClient

from app.main import app
from dashboard.dashboard_routes import build_health_rows
from services.copilot_engine import ask_llm


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


def test_build_health_rows_renders_risk_icons():
    foresight = {
        "anomalies": {
            "AMF": {
                "cpu_usage": {"risk": "HIGH"},
                "latency_ms": {"risk": "LOW"},
            }
        }
    }

    html = build_health_rows(foresight)

    assert "AMF" in html
    assert "🔴" in html
    assert "HIGH" in html


def test_ask_llm_returns_friendly_message_when_ollama_is_unavailable(monkeypatch):
    def raise_connection_error(*args, **kwargs):
        raise requests.exceptions.ConnectionError("Connection refused")

    monkeypatch.setattr("services.copilot_engine.requests.post", raise_connection_error)

    response = ask_llm("Is the network healthy?", {"network_status": "healthy", "root_cause": {}})

    assert "AI service is unavailable" in response
    assert "Ollama" in response
