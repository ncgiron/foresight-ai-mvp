"""
===========================================================
Foresight Engine

Purpose
-------
Aggregate all intelligence services into a
single network-health context.

Consumed By
-----------
- Dashboard
- API Clients
- Future LLM Copilot

Combines
--------
Anomalies
Correlation
Root Cause
Forecast
Recommendations
===========================================================
"""

from services.correlation_engine import correlate
from services.root_cause_engine import diagnose
from services.recommendation_engine import (
    generate_recommendations
)
from services.forecast_engine import (
    forecast_network
)


def build_foresight_context(
    anomalies: dict,
    historical_timeseries: dict
):

    correlation = correlate(
        anomalies
    )

    root_cause = diagnose(
        correlation
    )

    recommendations = (
        generate_recommendations(
            root_cause
        )
    )

    forecast = forecast_network(
        historical_timeseries
    )

    return {

        "network_status":

            root_cause.get(
                "status",
                "unknown"
            ),

        "anomalies":
            anomalies,

        "correlation":
            correlation,

        "root_cause":
            root_cause,

        "forecast":
            forecast,

        "recommendations":
            recommendations
    }