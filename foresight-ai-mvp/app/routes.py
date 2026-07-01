import datetime

from fastapi import APIRouter
from mock.kpi_generator import generate_timeseries ,generate_all_nodes
from services.telecom_engine import analyze_node
from services.topology import TOPOLOGY

router = APIRouter()

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
    return generate_all_nodes()
     

@router.get("/kpi/nodes/analysis")
def analyze_network():
    data = generate_all_nodes()

    results = []
    for node in data["nodes"].values():
        results.append(analyze_node(node))

    return {
        "timestamp": data["timestamp"],
        "analysis": results
    }

@router.get("/kpi/network/impact")
def network_impact():
    data = generate_all_nodes()

    impacts = {}

    for node, kpi in data["nodes"].items():
        result = analyze_node(kpi)

        impacts[node] = {
            "analysis": result,
            "depends_on": TOPOLOGY[node]
        }

    return {
        "timestamp": data["timestamp"],
        "impact_model": impacts
    }