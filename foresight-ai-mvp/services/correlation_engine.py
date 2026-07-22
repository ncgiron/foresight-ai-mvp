"""
===========================================================
Correlation Engine

Purpose
-------
Correlates KPI anomalies and identifies the most
likely root cause within the telecom network.

Input
-----
Anomaly results from anomaly_engine.py

Output
------
Root cause candidate
Confidence score
Evidence list

Future Enhancements
-------------------
- Topology-aware scoring
- Multi-node dependency analysis
- Probabilistic root cause analysis
- AI explanations
===========================================================
"""


def correlate(anomalies: dict):

    results = {}

    for node, metrics in anomalies.items():

        score = 0

        evidence = []
         # temporary debug print for correlation engine
        # print("NODE:", node)
        # print(metrics)
        # print(node, metrics["latency_ms"]["risk"])
        # CPU
        if metrics["cpu_usage"]["risk"] == "HIGH":
            score += 3
            evidence.append(
                "CPU anomaly detected"
            )

        # Latency
        if metrics["latency_ms"]["risk"] == "HIGH":
            score += 4
            evidence.append(
                "Latency anomaly detected"
            )

        # Memory
        if metrics["memory_usage"]["risk"] == "HIGH":
            score += 2
            evidence.append(
                "Memory anomaly detected"
            )

        # Throughput
        if metrics["throughput_mbps"]["risk"] == "HIGH":
            score += 2
            evidence.append(
                "Traffic increase detected"
            )

        # Sessions
        if metrics["sessions"]["risk"] == "HIGH":
            score += 2
            evidence.append(
                "Session load anomaly"
            )

        results[node] = {
            "score": score,
            "evidence": evidence
        }
        
        # temporary debug print for correlation engine
        print("SCORE:", node, score, evidence)
        print("RESULTS:", results)

    return determine_root_cause(results)

def determine_root_cause(correlation_results):

    best_node = None
    best_score = -1

    for node, result in correlation_results.items():

        if result["score"] > best_score:

            best_score = result["score"]
            best_node = node

    if best_score == 0:

        return {
            "status": "healthy",
            "root_cause": None,
            "confidence": 0,
            "score": 0,
            "evidence": []
        }

    confidence = min(
        95,
        best_score * 10
    )

    return {
        "status": "anomaly_detected",
        "root_cause": best_node,
        "confidence": confidence,
        "score": best_score,
        "evidence": correlation_results[best_node][
            "evidence"
        ]
    }