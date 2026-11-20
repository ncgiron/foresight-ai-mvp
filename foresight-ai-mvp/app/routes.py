import datetime
from multiprocessing import context
from fastapi import APIRouter
from fastapi import Depends
# from mock.kpi_generator import generate_timeseries ,generate_all_nodes
from services.telecom_engine import analyze_node
from services.topology import TOPOLOGY
from services.anomaly_engine import detect_anomaly
from services.correlation_engine import correlate
from mock.scenarios import apply_scenario
from services.root_cause_engine import diagnose
from services.correlation_engine import correlate
from services.forecast_engine import forecast_network
from services.recommendation_engine import generate_recommendations
from services.foresight_engine import build_foresight_context
from fastapi import Body
from services.copilot_engine import (ask_llm)
from services.foresight_engine import ( build_foresight_context)
from services.scenario_store import (
    set_current_scenario,
    get_current_scenario,
    get_scenario_data,
    apply_scenario_overrides
)
from mock.kpi_generator import (
    generate_timeseries,
    generate_timeseries_interval,
    generate_snapshot
)

from sqlalchemy.orm import Session
from app.core.database import get_db
from repositories.incident_repository import IncidentRepository
from services.incidents.similarity import find_similar_incidents

router = APIRouter()


def build_anomalies():
    """Build anomaly data from current snapshot and historical KPI trends."""

    current = generate_snapshot()
    historical = generate_timeseries(72)

    anomalies = {}

    for node_name, node_data in current["nodes"].items():
        history = {
            "cpu_usage": [
                sample["cpu_usage"]
                for sample in historical["timeseries"][node_name]
            ],
            "latency_ms": [
                sample["latency_ms"]
                for sample in historical["timeseries"][node_name]
            ],
            "sessions": [
                sample["sessions"]
                for sample in historical["timeseries"][node_name]
            ],
            "memory_usage": [
                sample["memory_usage"]
                for sample in historical["timeseries"][node_name]
            ],
            "throughput_mbps": [
                sample["throughput_mbps"]
                for sample in historical["timeseries"][node_name]
            ]
        }

                
        current_kpi = {

            "cpu_usage": node_data["cpu_usage"],
            "latency_ms": node_data["latency_ms"],
            "sessions": node_data["sessions"],
            "memory_usage": node_data["memory_usage"],
            "throughput_mbps": node_data["throughput_mbps"]
        }

        # Apply selected scenario BEFORE anomaly detection
        scenario = get_scenario_data()
        print("CURRENT SCENARIO:", get_current_scenario())
        print("NODE NAME:", node_name)
        print("SCENARIO:", scenario)
        print("NODE IN SCENARIO?", node_name in scenario)

        if node_name in scenario:

            for metric, value in scenario[node_name].items():

                current_kpi[metric] = value
        
        print("NODE:", node_name)
        print("CURRENT KPI:", current_kpi)

        anomalies[node_name] = detect_anomaly(
            history,
            current_kpi
        )
        
        print("ANOMALIES:", anomalies) 
               
    return anomalies

@router.get("/kpi/timeseries")
def get_timeseries(minutes: int | None = None, days: int = 7):
    """Return KPI time-series data, optionally at a specific interval over days."""
    if minutes is not None:
        data = generate_timeseries_interval(minutes, days)
    else:
        data = generate_timeseries()

    data["timeseries"] = apply_scenario_overrides(data["timeseries"])
    return data

@router.get("/kpi/nodes")
def get_nodes():
    """Return a current KPI snapshot for all network nodes."""
    # return generate_all_nodes()
    return generate_snapshot()
     

@router.get("/kpi/nodes/analysis")
def analyze_network():
    """Analyze the current network snapshot and return per-node results."""

    data = generate_snapshot()

    results = []

    for node_name, node_data in data["nodes"].items():

        node_data["node"] = node_name

        results.append(
            analyze_node(node_data)
        )

    return {
        "generated_at": data["generated_at"],
        "analysis": results
    }

@router.get("/kpi/network/impact")
def network_impact():
    """Return network impact analysis for all nodes based on current KPIs."""
    # data = generate_all_nodes()
    data =  generate_snapshot()

    impacts = {}

    for node, kpi in data["nodes"].items():

        kpi["node"] = node

        result = analyze_node(kpi)

        impacts[node] = {
            "analysis": result,
            "depends_on": TOPOLOGY[node]
        }
    
    return {
    "generated_at": data["generated_at"],
    "impact_model": impacts
    }
    

@router.get("/kpi/anomalies")
def get_anomalies():
    """Return anomaly detection results for the latest KPI snapshot."""

    return {
        "generated_at": datetime.datetime.utcnow().isoformat(),
        "anomalies": build_anomalies()
    }

@router.get("/kpi/correlation")
def get_correlation():
    """Return correlated anomaly data using the current anomaly set."""

    return correlate(
        build_anomalies()
    )


@router.get("/kpi/root-cause")
def get_root_cause():
    """Return root cause analysis based on current correlated anomalies."""

    correlation = correlate(
        build_anomalies()
    )

    return diagnose(
        correlation
    )

@router.get("/kpi/forecast")
def get_forecast():
    """Return a forecast of future KPI trends based on historical data."""

    historical = generate_timeseries(72)

    forecast = forecast_network(
        historical["timeseries"]
    )

    return {

        "generated_at":
            datetime.datetime.utcnow().isoformat(),

        "forecast":
            forecast
    }

@router.get("/kpi/recommendations")
def get_recommendations():
    """Return operational recommendations based on root cause analysis."""

    anomalies = build_anomalies()

    correlation = correlate(
        anomalies
    )

    root_cause = diagnose(
        correlation
    )

    recommendations = generate_recommendations(
        root_cause
    )

    return {

        "root_cause":
            root_cause,

        "recommendations":
            recommendations
    }


@router.get("/kpi/foresight")
def get_foresight():
    """Return a foresight context including anomalies and historical trends."""

    anomalies = build_anomalies()

    historical = generate_timeseries(
        72
    )

    return build_foresight_context(

        anomalies,

        historical["timeseries"]
    )





@router.post("/copilot/ask")
def ask_copilot(
    payload: dict = Body(...),
    db: Session = Depends(get_db)):
    
    """Ask the Copilot engine a question based on current anomaly context."""
    
    print("ACTIVE SCENARIO IN COPILOT:", get_current_scenario())
    question = payload["question"]
    anomalies = build_anomalies()
    historical = generate_timeseries(72)
    foresight = build_foresight_context(

        anomalies,

        historical["timeseries"]
    )
    print("=" * 80)
    print("FORESIGHT STATUS:", foresight.get("network_status"))
    print("ROOT CAUSE:", foresight.get("root_cause"))
    print("=" * 80)

    repo = IncidentRepository(db)

    incidents = repo.list()

    # similar_incidents = find_similar_incidents(incidents,question)

    root = foresight.get("root_cause", {})

    search_context = " ".join([
        question,
        str(root.get("root_cause", "")),
        str(root.get("diagnosis", "")),
        " ".join(root.get("evidence", []))
    ])

    similar_incidents = find_similar_incidents(
        incidents,
        search_context
    )

    print("SEARCH CONTEXT:", search_context)



  
    foresight["historical_incidents"] = similar_incidents
    
    answer = ask_llm(

        question,
        foresight
        # {"status": "ok"}
    )
    # print("Historical Incidents Found:")
    # print(similar_incidents)

    # print("HISTORICAL INCIDENTS:")
    # print(similar_incidents)

    print("=" * 80)
    print("QUESTION:", question)
    print("TOTAL INCIDENTS:", len(incidents))
    print("SIMILAR INCIDENTS FOUND:", len(similar_incidents))
    print(similar_incidents)
    print("=" * 80)

    

    return {

        "question":
            question,

        "answer":
            answer
    }

     
@router.post("/scenario/set")
def set_scenario(payload: dict):
    """Set the active scenario from the dashboard control payload."""

    scenario = payload["scenario"]

    print("REQUESTED:", scenario)

    result = set_current_scenario(scenario)

    print("RESULT:", result)

    return {"scenario": result}
    
@router.get("/scenario/current")
def get_scenario():
    """Return the currently active scenario name."""
    print("GET CURRENT:", get_current_scenario())
    return {
        "scenario": get_current_scenario()
    }


@router.get("/scenario/list")
def list_scenarios():
    """Return available scenario templates and metadata."""
    from services.scenario_store import SCENARIOS

    return {
        "scenarios": [
            {
                "name": name,
                "severity": meta.get("severity"),
                "description": meta.get("description"),
                "affected_nodes": meta.get("affected_nodes", []),
            }
            for name, meta in SCENARIOS.items()
        ]
    }