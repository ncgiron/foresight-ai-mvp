
"""
===========================================================
Plot Utilities

Purpose
-------
Generate interactive Plotly charts from telecom KPI data.

This module contains NO FastAPI logic.

Its responsibility is only:

Input
-----
Python dictionaries containing KPI history

Output
------
Plotly Figure objects

Future Improvements
-------------------
- AI anomaly indicators
- Capacity forecasts
- Confidence intervals
- Correlation overlays
- Root cause highlighting
===========================================================
"""

import plotly.graph_objects as go


def cpu_chart(timeseries):
    """
    Create CPU utilisation chart.

    Parameters
    ----------
    timeseries : dict
        KPI history for all network functions.

    Returns
    -------
    Plotly Figure
    """

    fig = go.Figure()

    # Plot CPU history for each network function
    for node, values in timeseries.items():

        fig.add_trace(

            go.Scatter(
                x=[v["timestamp"] for v in values],
                y=[v["cpu_usage"] for v in values],
                mode="lines",
                name=node
            )

        )

    fig.update_layout(

        title="CPU Usage per Network Function",

        xaxis_title="Time",

        yaxis_title="CPU (%)"

    )

    return fig


def sessions_chart(timeseries):
    """
    Create active sessions chart.

    Shows subscriber load variation throughout
    the simulated day.
    """

    fig = go.Figure()

    for node, values in timeseries.items():

        fig.add_trace(

            go.Scatter(
                x=[v["timestamp"] for v in values],
                y=[v["sessions"] for v in values],
                mode="lines",
                name=node
            )

        )

    fig.update_layout(

        title="Active Sessions",

        xaxis_title="Time",

        yaxis_title="Sessions"

    )

    return fig


def latency_chart(timeseries):
    """
    Create latency trend chart.

    Useful for identifying performance
    degradation and future anomaly detection.
    """

    fig = go.Figure()

    for node, values in timeseries.items():

        fig.add_trace(

            go.Scatter(
                x=[v["timestamp"] for v in values],
                y=[v["latency_ms"] for v in values],
                mode="lines",
                name=node
            )

        )

    fig.update_layout(

        title="Latency per Network Function",

        xaxis_title="Time",

        yaxis_title="Latency (ms)"

    )

    return fig


def throughput_chart(timeseries):
    """
    Create throughput chart.

    Represents traffic carried by each
    network function over time.

    Future versions may include:
    - Forecast values
    - Congestion prediction
    - Capacity thresholds
    """

    fig = go.Figure()

    for node, values in timeseries.items():

        fig.add_trace(

            go.Scatter(
                x=[v["timestamp"] for v in values],
                y=[v["throughput_mbps"] for v in values],
                mode="lines",
                name=node
            )

        )

    fig.update_layout(

        title="Network Throughput",

        xaxis_title="Time",

        yaxis_title="Throughput (Mbps)"

    )

    return fig


def calculate_summary(timeseries):

    peak_cpu = 0
    peak_sessions = 0
    peak_throughput = 0

    latencies = []

    for node_values in timeseries.values():

        for sample in node_values:

            peak_cpu = max(
                peak_cpu,
                sample["cpu_usage"]
            )

            peak_sessions = max(
                peak_sessions,
                sample["sessions"]
            )

            peak_throughput = max(
                peak_throughput,
                sample["throughput_mbps"]
            )

            latencies.append(
                sample["latency_ms"]
            )

    avg_latency = round(
        sum(latencies) / len(latencies),
        2
    )

    return {

        "peak_cpu": peak_cpu,

        "peak_sessions": peak_sessions,

        "peak_throughput": peak_throughput,

        "average_latency": avg_latency
    }