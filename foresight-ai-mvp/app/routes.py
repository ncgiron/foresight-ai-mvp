import datetime

from fastapi import APIRouter
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

from services.scenario_store import (set_current_scenario, get_current_scenario)
from mock.kpi_generator import (generate_timeseries, generate_snapshot)
from services.scenario_store import get_scenario_data


router = APIRouter()
#debugging temporary print statements

print(
    "SCENARIO OBJECT ID:",
    id(get_current_scenario)
)

print(
    "CURRENT SCENARIO:",
    get_current_scenario()
)
#=========================
def build_anomalies():

    current = generate_snapshot()
    # current = apply_scenario(current, "upf_congestion")

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

    
# # Apply selected scenario overrides
#         scenario = get_scenario_data()
        
#         print("ACTIVE SCENARIO:", get_current_scenario())
#         print("SCENARIO DATA:", scenario)

#     for nf, metrics in scenario.items():
#         if nf not in anomalies:
#             continue
#         for metric, value in metrics.items():
#             if metric in anomalies[nf]:
#                 anomalies[nf][metric]["value"] = value
                
    return anomalies


# @router.get("/kpi/nodes")
# def get_all_nodes():
#     return generate_all_nodes()


# @router.get("/kpi/nodes/analysis")
# def analyze_all_nodes():

#     nodes = generate_all_nodes()

#     return {
#         "results": [analyze_node(n) for n in nodes]
#     }
@router.get("/kpi/timeseries")
def get_timeseries():
    return generate_timeseries()

@router.get("/kpi/nodes")
def get_nodes():
    # return generate_all_nodes()
    return generate_snapshot()
     

@router.get("/kpi/nodes/analysis")
def analyze_network():

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

    # return {
    #     "timestamp": data["timestamp"],
    #     "impact_model": impacts
    # }
    
    return {
    "generated_at": data["generated_at"],
    "impact_model": impacts
    }
    

@router.get("/kpi/anomalies")
def get_anomalies():

    return {
        "generated_at": datetime.datetime.utcnow().isoformat(),
        "anomalies": build_anomalies()
    }

@router.get("/kpi/correlation")
def get_correlation():

    return correlate(
        build_anomalies()
    )


@router.get("/kpi/root-cause")
def get_root_cause():

    correlation = correlate(
        build_anomalies()
    )

    return diagnose(
        correlation
    )

@router.get("/kpi/forecast")
def get_forecast():

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

    anomalies = build_anomalies()

    historical = generate_timeseries(
        72
    )

    return build_foresight_context(

        anomalies,

        historical["timeseries"]
    )


@router.post("/copilot/ask")
def ask_copilot( payload: dict = Body(...)):
    
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
    
    answer = ask_llm(

        question,

        foresight
        # {"status": "ok"}
    )

    return {

        "question":
            question,

        "answer":
            answer
    }

# @router.post("/scenario/set")
# def set_scenario(payload: dict):

#     scenario = payload["scenario"]

#     return {
#         "scenario": set_current_scenario(scenario)
#     }
   
# @router.post("/scenario/set")
# def set_scenario(payload: dict):

#     scenario = payload["scenario"]

#     result = set_current_scenario(scenario)

#     print("SET SCENARIO:", result)

#     return {
#         "scenario": result
#     }
     
@router.post("/scenario/set")
def set_scenario(payload: dict):

    scenario = payload["scenario"]

    print("REQUESTED:", scenario)

    result = set_current_scenario(scenario)

    print("RESULT:", result)

    return {"scenario": result}
    
@router.get("/scenario/current")
def get_scenario():
    print("GET CURRENT:", get_current_scenario())
    return {
        "scenario": get_current_scenario()
    }