import numpy as np

def compute_zscore(values, current):
    if len(values) < 5:
        return 0

    mean = np.mean(values)
    std = np.std(values)

    if std == 0:
        return 0
    #### temporary fix for UPF CPU anomaly detection
    

    return (current - mean) / std


def detect_anomaly(kpi_history, current_kpi):
    result = {}

    for metric, value in current_kpi.items():
        if metric in ["node"]:
            continue

        history = kpi_history.get(metric, [])

        z = compute_zscore(history, value)

        if abs(z) > 3:
            risk = "HIGH"
        elif abs(z) > 2:
            risk = "MEDIUM"
        else:
            risk = "LOW"

        # result[metric] = {
        #     "value": value,
        #     "z_score": z,
        #     "risk": risk
        # }
        
        result[metric] = {

        "value": round(value, 2),

        "z_score": round(z, 2),

        "direction":
            "HIGH" if z > 0 else "LOW",

        "risk": risk
        }

    return result

def summarize_node_anomalies(result):

    highest = "LOW"

    for metric in result.values():

        if metric["risk"] == "HIGH":
            highest = "HIGH"
            break

        elif metric["risk"] == "MEDIUM":
            highest = "MEDIUM"

    return highest