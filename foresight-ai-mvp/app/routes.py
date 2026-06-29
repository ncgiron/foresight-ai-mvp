from fastapi import APIRouter
from mock.kpi_generator import generate_all_nodes
from services.telecom_engine import analyze_node

router = APIRouter()

@router.get("/kpi/nodes")
def get_all_nodes():
    return generate_all_nodes()


@router.get("/kpi/nodes/analysis")
def analyze_all_nodes():

    nodes = generate_all_nodes()

    return {
        "results": [analyze_node(n) for n in nodes]
    }