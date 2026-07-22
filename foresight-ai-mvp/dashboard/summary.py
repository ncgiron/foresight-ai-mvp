"""
===========================================================
Dashboard Summary Utilities

Purpose
-------
Calculate high-level KPI statistics for display
on the Telecom AI Dashboard.

Current Metrics
---------------
- Peak CPU
- Peak Sessions
- Peak Throughput
- Average Latency

Future Enhancements
-------------------
- Average CPU
- Busy-hour metrics
- Node-specific summaries
- Capacity utilization
===========================================================
"""


def calculate_summary(timeseries):
    """
    Calculate dashboard KPI summary statistics.

    Parameters
    ----------
    timeseries : dict
        Time-series KPI data for all network functions.

    Returns
    -------
    dict
        Summary metrics used by the dashboard.
    """

    summary = {
        "peak_cpu": 0,
        "peak_sessions": 0,
        "peak_throughput": 0,
        "average_latency": 0
    }

    total_latency = 0
    total_points = 0

    # Iterate through all nodes and KPI samples
    for node, values in timeseries.items():

        for sample in values:

            summary["peak_cpu"] = max(
                summary["peak_cpu"],
                sample["cpu_usage"]
            )

            summary["peak_sessions"] = max(
                summary["peak_sessions"],
                sample["sessions"]
            )

            summary["peak_throughput"] = max(
                summary["peak_throughput"],
                sample["throughput_mbps"]
            )

            total_latency += sample["latency_ms"]

            total_points += 1

    # Calculate average latency
    if total_points > 0:
        summary["average_latency"] = (
            total_latency / total_points
        )

    return summary