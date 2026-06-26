def analyze_kpi(kpi: dict):

    cpu = kpi.get("cpu", 0)
    memory = kpi.get("memory", 0)
    sessions = kpi.get("active_sessions", 0)

    risk = "LOW"
    score = 100

    if cpu > 85:
        risk = "HIGH"
        score -= 30

    if memory > 85:
        risk = "HIGH"
        score -= 20

    if sessions > 4500000:
        risk = "MEDIUM"
        score -= 15

    return {
        "health_score": max(score, 0),
        "risk_level": risk,
        "recommendation": generate_recommendation(risk, score)
    }


def generate_recommendation(risk, score):

    if risk == "HIGH":
        return "Immediate investigation required. Scale resources or redistribute traffic."

    if score < 70:
        return "Monitor closely. Potential capacity degradation."

    return "System operating within normal parameters."