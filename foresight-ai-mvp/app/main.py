from fastapi import FastAPI ,Depends
from sqlalchemy.orm import Session

from app.routes import router
from services.telecom_engine import analyze_node
from mock.fake_foresight import get_fake_kpi
from dashboard.dashboard_routes import router as dashboard_router
from services.history_store import HISTORY 
from services.anomaly_engine import detect_anomaly
from services.history_service import  HistoryService

from app.models import KPIHistory
from app.core.database import Base, get_db
from app.core.database import engine



from app.api.history import router as history_router

Base.metadata.create_all(bind=engine)








app = FastAPI(
    title="Foresight AI MVP",
    description="Telecom KPI Analytics Prototype using Fake Foresight Data",
    version="0.1.0"
)

app.include_router(router)
app.include_router(dashboard_router)
app.include_router(history_router)


@app.get("/")
def root():
    return {
        "message": "Foresight AI MVP is running",
        "docs": "/docs",
        "health": "/health"
    }
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

def get_smf_kpi(
    db: Session = Depends(get_db)
):
    kpi = get_fake_kpi()

    HistoryService.store_kpi(
        db=db,
        node=kpi
    )

    return kpi


    # return get_fake_kpi()


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
    analysis = analyze_node(kpi)

    return {
        "node": kpi["node"],
        "kpi": kpi,
        "analysis": analysis
    }