import random
from datetime import datetime

NODES = ["AMF01", "SMF01", "UPF01"]

def generate_kpi(node: str):

    base_cpu = random.randint(40, 90)
    base_mem = random.randint(30, 95)

    # simulate telecom behaviour differences per node
    if "AMF" in node:
        sessions = random.randint(2000000, 6000000)
        throughput = random.randint(10, 40)

    elif "SMF" in node:
        sessions = random.randint(3000000, 8000000)
        throughput = random.randint(50, 120)

    else:  # UPF
        sessions = random.randint(1000000, 4000000)
        throughput = random.randint(100, 300)

    return {
        "node": node,
        "cpu": base_cpu,
        "memory": base_mem,
        "active_sessions": sessions,
        "throughput_gbps": throughput,
        "packet_loss": round(random.uniform(0.01, 0.5), 2),
        "timestamp": datetime.utcnow().isoformat()
    }


def generate_all_nodes():
    return [generate_kpi(node) for node in NODES]