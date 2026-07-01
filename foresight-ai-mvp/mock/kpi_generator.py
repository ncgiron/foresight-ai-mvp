import random
from datetime import datetime, timedelta

NODES = ["AMF", "SMF", "UPF", "PCF"]

def generate_all_nodes():
    data = {}

    for node in NODES:
        base_load = random.uniform(40, 70)

        data[node] = {
            "node": node,
            "cpu_usage": min(100, base_load + random.uniform(-10, 25)),
            "memory_usage": min(100, base_load + random.uniform(-5, 20)),
            "throughput_mbps": random.uniform(100, 2000),
            "sessions": int(random.uniform(1000, 50000)),
            "latency_ms": random.uniform(5, 80),
        }

    return {
        "timestamp": "2026-06-29T00:00:00Z",
        "nodes": data
    }

def _traffic_profile(hour: int):
    """
    Simulates telecom daily traffic curve
    """
    if 6 <= hour < 10:
        return 0.6  # morning ramp
    elif 10 <= hour < 14:
        return 1.0  # peak
    elif 14 <= hour < 17:
        return 0.8
    elif 17 <= hour < 21:
        return 1.1  # evening peak
    else:
        return 0.3  # night low


def generate_timeseries(hours: int = 24):
    base_time = datetime(2026, 6, 29, 0, 0)

    data = {node: [] for node in NODES}

    for h in range(hours):
        timestamp = base_time + timedelta(hours=h)
        factor = _traffic_profile(h)

        for node in NODES:

            noise = random.uniform(0.9, 1.1)

            if node == "AMF":
                sessions = int(20000 * factor * noise)
                cpu = min(100, 40 + factor * 50 * noise)

            elif node == "SMF":
                sessions = int(15000 * factor * noise)
                cpu = min(100, 35 + factor * 55 * noise)

            elif node == "UPF":
                sessions = int(12000 * factor * noise)
                cpu = min(100, 30 + factor * 60 * noise)

            else:  # PCF
                sessions = int(8000 * factor * noise)
                cpu = min(100, 25 + factor * 30 * noise)

            data[node].append({
                "timestamp": timestamp.isoformat(),
                "cpu_usage": round(cpu, 2),
                "sessions": sessions,
                "traffic_factor": factor
            })

    return {
        "generated_at": datetime.utcnow().isoformat(),
        "timeseries": data
    }