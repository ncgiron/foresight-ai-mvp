# def get_fake_kpi():
#     return {
#         "node": "SMF01",
#         "technology": "5G Core",
#         "cpu": 78,
#         "memory": 62,
#         "active_sessions": 4200000,
#         "throughput_gbps": 115,
#         "packet_loss": 0.02,
#         "timestamp": "2026-06-26T10:00:00Z"
#     }


from mock.kpi_generator import generate_snapshot


def get_fake_kpi():
    """
    Simulate a Foresight KPI response.

    Returns
    -------
    dict
    """

    snapshot = generate_snapshot()

    smf = snapshot["nodes"]["SMF"]

    return {

        "node": "SMF01",

        "technology": "5G Core",

        "cpu": smf["cpu_usage"],

        "memory": smf["memory_usage"],

        "active_sessions": smf["sessions"],

        "throughput_gbps": smf["throughput_mbps"],

        "packet_loss": 0.02,

        "timestamp": smf["timestamp"]
    }