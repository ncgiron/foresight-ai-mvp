"""
===========================================================
Forecast Engine

Purpose
-------
Predict near-future KPI behaviour based on
historical trends.

Inputs
------
Historical KPI series

Outputs
-------
Predicted KPI values
Risk assessment
Threshold proximity

Future Enhancements
-------------------
- Linear Regression
- ARIMA
- Prophet
- LSTM
- Capacity Forecasting
===========================================================
"""


def forecast_metric(history, threshold=None):

    if len(history) < 6:

        current = history[-1]

        return {
            "current": round(current, 2),
            "predicted": round(current, 2),
            "risk": "UNKNOWN"
        }

    recent = history[-6:]

    current = recent[-1]

    trend = (
        recent[-1]
        - recent[0]
    ) / len(recent)

    predicted = current + trend

    risk = "LOW"

    if threshold is not None:

        if predicted >= threshold:

            risk = "HIGH"

        elif predicted >= threshold * 0.9:

            risk = "MEDIUM"

    return {

        "current":
            round(current, 2),

        "predicted":
            round(predicted, 2),

        "trend":
            round(trend, 2),

        "threshold":
            threshold,

        "risk":
            risk
    }


def forecast_node(node_history):

    thresholds = {

        "cpu_usage": 90,

        "memory_usage": 90,

        "latency_ms": 50,

        "sessions": 50000,

        "throughput_mbps": 5000
    }

    forecast = {}

    for metric, values in node_history.items():

        forecast[metric] = forecast_metric(

            values,

            thresholds.get(metric)
        )

    return forecast


def forecast_network(timeseries):

    results = {}

    for node_name, node_data in timeseries.items():

        history = {

            "cpu_usage": [
                sample["cpu_usage"]
                for sample in node_data
            ],

            "memory_usage": [
                sample["memory_usage"]
                for sample in node_data
            ],

            "latency_ms": [
                sample["latency_ms"]
                for sample in node_data
            ],

            "sessions": [
                sample["sessions"]
                for sample in node_data
            ],

            "throughput_mbps": [
                sample["throughput_mbps"]
                for sample in node_data
            ]
        }

        results[node_name] = forecast_node(
            history
        )

    return results