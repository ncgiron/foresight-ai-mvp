import random
from datetime import datetime, timedelta



NODES = ["AMF", "SMF", "UPF", "PCF"]

# def generate_all_nodes():
#     data = {}

#     for node in NODES:
#         base_load = random.uniform(40, 70)

#         data[node] = {
#             "node": node,
#             "cpu_usage": min(100, base_load + random.uniform(-10, 25)),
#             "memory_usage": min(100, base_load + random.uniform(-5, 20)),
#             "throughput_mbps": random.uniform(100, 2000),
#             "sessions": int(random.uniform(1000, 50000)),
#             "latency_ms": random.uniform(5, 80),
#         }

#     return {
#         "timestamp": "2026-06-29T00:00:00Z",
#         "nodes": data
#     }

def generate_all_nodes():
    """
    Return the most recent KPI snapshot.

    Reuses the time-series generator so both APIs
    produce consistent data.
    """

    ts = generate_timeseries(hours=72)

    latest = {}

    for node, history in ts["timeseries"].items():
        latest[node] = history[-1]

    return {
        "timestamp": ts["generated_at"],
        "nodes": latest
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





def generate_timeseries(hours: int = 72):
    """
    Generate a realistic 24-hour telecom traffic simulation.

    The KPIs are correlated instead of random.

    Traffic
        ↓
    Sessions
        ↓
    CPU
        ↓
    Memory
        ↓
    Latency
        ↓
    Throughput

    This is much closer to what would be received
    from a monitoring platform such as Foresight.
    """

    base_time = datetime(2026, 6, 29, 0, 0)

    data = {node: [] for node in NODES}

    for hour in range(hours):

        timestamp = base_time + timedelta(hours=hour)

        traffic = _traffic_profile(hour)

        for node in NODES:

            # Small random variation to avoid identical curves
            noise = random.uniform(0.95, 1.05)

            # ---------------------------------------------------
            # Node-specific engineering profiles
            # ---------------------------------------------------

            if node == "AMF":

                base_sessions = 22000
                cpu_multiplier = 55
                throughput_multiplier = 0.03

            elif node == "SMF":

                base_sessions = 18000
                cpu_multiplier = 60
                throughput_multiplier = 0.025

            elif node == "UPF":

                base_sessions = 15000
                cpu_multiplier = 65
                throughput_multiplier = 0.12

            else:  # PCF

                base_sessions = 9000
                cpu_multiplier = 35
                throughput_multiplier = 0.015

            # ---------------------------------------------------
            # Correlated KPI generation
            # ---------------------------------------------------

            sessions = int(base_sessions * traffic * noise)

            cpu = min(
                100,
                25 + traffic * cpu_multiplier * noise
            )

            memory = min(
                100,
                30 + cpu * 0.75 + random.uniform(-4, 4)
            )

            latency = (
                8
                + cpu * 0.20
                + random.uniform(-2, 2)
            )

            throughput = (
                sessions * throughput_multiplier
            )

            data[node].append({

                "timestamp": timestamp.isoformat(),

                "cpu_usage": round(cpu, 2),

                "memory_usage": round(memory, 2),

                "sessions": sessions,

                "throughput_mbps": round(throughput, 2),

                "latency_ms": round(latency, 2),

                "traffic_factor": traffic

            })

    return {

        "generated_at": datetime.utcnow().isoformat(),

        "timeseries": data

    }