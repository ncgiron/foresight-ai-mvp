def analyze_node(kpi: dict):

    cpu = kpi["cpu"]
    memory = kpi["memory"]
    sessions = kpi["active_sessions"]
    packet_loss = kpi["packet_loss"]

    score = 100
    risk = "LOW"

    # CPU stress model
    if cpu > 85:
        score -= 25
        risk = "HIGH"

    # Memory pressure
    if memory > 85:
        score -= 20
        risk = "HIGH"

    # Session overload (telecom realistic threshold)
    if sessions > 5000000:
        score -= 15
        if risk != "HIGH":
            risk = "MEDIUM"

    # Packet loss is critical in telecom
    if packet_loss > 0.2:
        score -= 30
        risk = "HIGH"

    return {
        "node": kpi["node"],
        "health_score": max(score, 0),
        "risk_level": risk,
        "recommendation": generate_recommendation(risk, score)
    }


def generate_recommendation(risk, score):

    if risk == "HIGH":
        return "CRITICAL: immediate traffic reroute or scaling required."

    if score < 70:
        return "WARNING: investigate capacity and session load."

    return "OK: system stable within expected thresholds."