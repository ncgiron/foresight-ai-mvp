"""
===========================================================
Root Cause Engine

Purpose
-------
Translate anomaly correlations into
telecom engineering diagnoses.

Input
-----
Correlation engine output

Output
------
Root cause diagnosis
Confidence
Evidence
Recommendation

Examples
--------
UPF Congestion
SMF Overload
AMF Registration Storm
PCF Policy Failure
===========================================================
"""


def diagnose(correlation_result: dict):

    node = correlation_result.get(
        "root_cause"
    )

    score = correlation_result.get(
        "score",
        0
    )

    evidence = correlation_result.get(
        "evidence",
        []
    )

    confidence = correlation_result.get(
        "confidence",
        0
    )

    if node is None:

        return {
            "status": "healthy",
            "diagnosis": "No significant anomalies detected",
            "confidence": 0,
            "recommendation": "No action required"
        }

    diagnosis = _map_diagnosis(
        node=node,
        score=score,
        evidence=evidence
    )

    return {

        "status": "root_cause_identified",

        "root_cause": node,

        "diagnosis":
            diagnosis["diagnosis"],

        "confidence":
            confidence,

        "impact":
            diagnosis["impact"],

        "recommendation":
            diagnosis["recommendation"],

        "evidence":
            evidence
    }


def _map_diagnosis(
    node,
    score,
    evidence
):

    if node == "UPF":

        return {

            "diagnosis":
                "User Plane Congestion",

            "impact":
                [
                    "Increased latency",
                    "Reduced user throughput",
                    "Packet forwarding degradation"
                ],

            "recommendation":
                (
                    "Scale UPF capacity, "
                    "redistribute traffic, "
                    "or investigate traffic spikes."
                )
        }

    elif node == "SMF":

        return {

            "diagnosis":
                "Session Management Overload",

            "impact":
                [
                    "Session establishment delays",
                    "Registration failures",
                    "Control plane degradation"
                ],

            "recommendation":
                (
                    "Review session load, "
                    "investigate signaling spikes, "
                    "and scale SMF resources."
                )
        }

    elif node == "AMF":

        return {

            "diagnosis":
                "Registration Storm or AMF Overload",

            "impact":
                [
                    "UE registration failures",
                    "Attach procedure delays",
                    "Control plane congestion"
                ],

            "recommendation":
                (
                    "Check registration traffic, "
                    "mobility events, "
                    "and AMF capacity."
                )
        }

    elif node == "PCF":

        return {

            "diagnosis":
                "Policy Control Degradation",

            "impact":
                [
                    "Policy delivery delays",
                    "QoS inconsistencies",
                    "Charging rule delays"
                ],

            "recommendation":
                (
                    "Review policy workflows, "
                    "database performance, "
                    "and PCF resource utilization."
                )
        }

    return {

        "diagnosis":
            "Unknown Condition",

        "impact":
            [],

        "recommendation":
            "Further investigation required."
    }