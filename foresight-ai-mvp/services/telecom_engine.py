# def analyze_node(kpi: dict):

#     cpu = kpi["cpu"]
#     memory = kpi["memory"]
#     sessions = kpi["active_sessions"]
#     packet_loss = kpi["packet_loss"]

#     score = 100
#     risk = "LOW"

#     # CPU stress model
#     if cpu > 85:
#         score -= 25
#         risk = "HIGH"

#     # Memory pressure
#     if memory > 85:
#         score -= 20
#         risk = "HIGH"

#     # Session overload (telecom realistic threshold)
#     if sessions > 5000000:
#         score -= 15
#         if risk != "HIGH":
#             risk = "MEDIUM"

#     # Packet loss is critical in telecom
#     if packet_loss > 0.2:
#         score -= 30
#         risk = "HIGH"

#     return {
#         "node": kpi["node"],
#         "health_score": max(score, 0),
#         "risk_level": risk,
#         "recommendation": generate_recommendation(risk, score)
#     }


# def analyze_node(node_kpi: dict):
#     cpu = node_kpi["cpu_usage"]
#     sessions = node_kpi["sessions"]
#     latency = node_kpi["latency_ms"]

#     risk = "LOW"

#     if cpu > 85 or latency > 60:
#         risk = "HIGH"
#     elif cpu > 70 or sessions > 30000:
#         risk = "MEDIUM"

#     return {
#         "node": node_kpi["node"],
#         "risk": risk,
#         "recommendation": "Scale UPF" if risk == "HIGH" else "Monitor"
#     }

# def generate_recommendation(risk, score):

#     if risk == "HIGH":
#         return "CRITICAL: immediate traffic reroute or scaling required."

#     if score < 70:
#         return "WARNING: investigate capacity and session load."

#     return "OK: system stable within expected thresholds."


def analyze_node(node_kpi: dict):
    cpu = node_kpi["cpu_usage"]
    latency = node_kpi["latency_ms"]
    sessions = node_kpi["sessions"]
    node = node_kpi["node"]

    score = 0

    # base risk
    if cpu > 85:
        score += 3
    elif cpu > 70:
        score += 2
    else:
        score += 1

    if latency > 60:
        score += 2

    if sessions > 30000:
        score += 2

    if score >= 6:
        risk = "HIGH"
    elif score >= 4:
        risk = "MEDIUM"
    else:
        risk = "LOW"

    return {
        "node": node,
        "risk": risk,
        "score": score,
        "recommendation": f"Investigate {node} capacity"
    }