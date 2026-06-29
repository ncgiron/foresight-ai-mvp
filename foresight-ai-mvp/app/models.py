from pydantic import BaseModel
from typing import Dict, List


class NodeKPI(BaseModel):
    node: str
    cpu_usage: float
    memory_usage: float
    throughput_mbps: float
    sessions: int
    latency_ms: float


class NetworkState(BaseModel):
    timestamp: str
    nodes: Dict[str, NodeKPI]