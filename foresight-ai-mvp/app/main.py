from fastapi import FastAPI
from services.engineering_engine import analyze_kpi
from mock.fake_foresight import get_fake_kpi

app = FastAPI(
    title="Foresight AI MVP",
    description="Telecom KPI Analytics Prototype using Fake Foresight Data",
    version="0.1.0"
)

# -----------------------------
# Health Check
# -----------------------------
@app.get("/health")
def health():
    return {
        "status": "running",
        "service": "foresight-ai-mvp"
    }


# -----------------------------
# Raw KPI (Mock Foresight API)
# -----------------------------
@app.get("/kpi/smf")
def get_smf_kpi():
    """
    Returns fake KPI data (simulates Foresight API)
    """
    return get_fake_kpi()


# -----------------------------
# KPI Analysis Endpoint
# -----------------------------
@app.get("/kpi/smf/analysis")
def smf_analysis():
    """
    End-to-end flow:
    Fake KPI → Engineering Engine → Result
    """
    kpi = get_fake_kpi()
    analysis = analyze_kpi(kpi)

    return {
        "node": kpi["node"],
        "kpi": kpi,
        "analysis": analysis
    }