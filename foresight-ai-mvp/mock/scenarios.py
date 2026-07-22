"""
===========================================================
Telecom Failure Scenarios

Purpose
-------
Inject realistic telecom failures into KPI snapshots.

Used By
-------
- Anomaly testing
- Correlation testing
- Root cause validation
- Demo environments

Examples
--------
UPF Congestion
SMF Overload
AMF Registration Storm
PCF Policy Failure
===========================================================
"""


def upf_congestion(node: dict):
    """
    Heavy UPF load causing
    user-plane congestion.
    """

    node["cpu_usage"] = 95
    node["memory_usage"] = 98
    node["latency_ms"] = 120

    return node


def smf_overload(node: dict):
    """
    Excessive session management load.
    """

    node["cpu_usage"] = 92
    node["memory_usage"] = 90
    node["sessions"] = 50000

    return node


def amf_registration_storm(node: dict):
    """
    Massive UE registration burst.
    """

    node["cpu_usage"] = 90
    node["sessions"] = 60000
    node["latency_ms"] = 80

    return node


def pcf_policy_failure(node: dict):
    """
    Policy processing degradation.
    """

    node["cpu_usage"] = 85
    node["memory_usage"] = 95
    node["latency_ms"] = 70

    return node


def site_failure(node: dict):
    """
    Severe node degradation.
    """

    node["cpu_usage"] = 99
    node["memory_usage"] = 99
    node["latency_ms"] = 200

    return node


def apply_scenario(snapshot: dict, scenario_name: str):
    """
    Apply scenario to snapshot.
    """

    if scenario_name == "upf_congestion":

        snapshot["nodes"]["UPF"] = upf_congestion(
            snapshot["nodes"]["UPF"]
        )

    elif scenario_name == "smf_overload":

        snapshot["nodes"]["SMF"] = smf_overload(
            snapshot["nodes"]["SMF"]
        )

    elif scenario_name == "amf_registration_storm":

        snapshot["nodes"]["AMF"] = amf_registration_storm(
            snapshot["nodes"]["AMF"]
        )

    elif scenario_name == "pcf_policy_failure":

        snapshot["nodes"]["PCF"] = pcf_policy_failure(
            snapshot["nodes"]["PCF"]
        )

    elif scenario_name == "site_failure":

        for node in snapshot["nodes"]:

            snapshot["nodes"][node] = site_failure(
                snapshot["nodes"][node]
            )

    return snapshot