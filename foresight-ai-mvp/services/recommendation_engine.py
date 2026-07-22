"""
===========================================================
Recommendation Engine

Purpose
-------
Generate operational recommendations based on

- Root Cause
- Confidence
- Forecast Risk

Input
-----
Root Cause Analysis Output

Output
------
Recommended Actions
Priority
Operational Guidance

Future Enhancements
-------------------
- Runbook Integration
- Ticket Generation
- Change Recommendations
- AI Assisted Actions
===========================================================
"""


def generate_recommendations(root_cause_result: dict):

    status = root_cause_result.get(
        "status"
    )

    if status == "healthy":

        return {
            "priority": "NONE",
            "actions": [
                "No action required."
            ]
        }

    root_cause = root_cause_result.get(
        "root_cause"
    )

    confidence = root_cause_result.get(
        "confidence",
        0
    )

    if root_cause == "UPF":

        return _upf_actions(confidence)

    elif root_cause == "SMF":

        return _smf_actions(confidence)

    elif root_cause == "AMF":

        return _amf_actions(confidence)

    elif root_cause == "PCF":

        return _pcf_actions(confidence)

    return {

        "priority": "MEDIUM",

        "actions": [
            "Investigate abnormal KPI behaviour."
        ]
    }


def _upf_actions(confidence):

    return {

        "priority": _priority(confidence),

        "actions": [

            "Review UPF CPU utilization.",

            "Review UPF memory utilization.",

            "Investigate traffic growth patterns.",

            "Verify traffic balancing across UPFs.",

            "Review recent configuration changes.",

            "Consider scaling UPF capacity.",

            "Inspect latency and packet-forwarding KPIs."
        ]
    }


def _smf_actions(confidence):

    return {

        "priority": _priority(confidence),

        "actions": [

            "Review session establishment rates.",

            "Verify SMF resource utilization.",

            "Inspect signalling load.",

            "Check recent subscriber growth.",

            "Investigate session management bottlenecks.",

            "Scale SMF resources if required."
        ]
    }


def _amf_actions(confidence):

    return {

        "priority": _priority(confidence),

        "actions": [

            "Review registration traffic levels.",

            "Check UE mobility events.",

            "Inspect AMF CPU utilization.",

            "Investigate registration storms.",

            "Validate AMF scaling configuration.",

            "Review recent software updates."
        ]
    }


def _pcf_actions(confidence):

    return {

        "priority": _priority(confidence),

        "actions": [

            "Review policy-control transactions.",

            "Inspect policy rule processing times.",

            "Validate PCF database performance.",

            "Check QoS policy delivery.",

            "Review charging-rule provisioning.",

            "Investigate recent policy changes."
        ]
    }


def _priority(confidence):

    if confidence >= 80:

        return "CRITICAL"

    if confidence >= 60:

        return "HIGH"

    if confidence >= 40:

        return "MEDIUM"

    return "LOW"