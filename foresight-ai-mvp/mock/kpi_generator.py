"""
===========================================================
KPI Generator

Purpose
-------
Generate realistic telecom KPI snapshots and
historical time-series data.

This module acts as the single source of truth
for KPI generation across the platform.

Public Functions
----------------
generate_snapshot()
generate_timeseries()

Internal Functions
------------------
_traffic_profile()
_node_profile()
_apply_noise()
_generate_node_metrics()
_build_snapshot()
_build_timeseries()

Future Improvements
-------------------
- Scenario simulation
- Traffic spikes
- Core failures
- Maintenance windows
- Capacity thresholds
===========================================================
"""

import random

from datetime import datetime
from datetime import timedelta


NODES = ["AMF", "SMF", "UPF", "PCF"]


# ==========================================================
# Public API
# ==========================================================

def generate_snapshot(timestamp=None):
    """
    Generate a single KPI snapshot.

    Used by
    -------
    - REST APIs
    - Historical Repository
    - Future KPI Collector

    Parameters
    ----------
    timestamp : datetime, optional

    Returns
    -------
    dict
    """

    if timestamp is None:
        timestamp = datetime.utcnow()

    return _build_snapshot(timestamp)


def generate_timeseries(hours: int = 72):
    """
    Generate KPI history for all nodes.

    Parameters
    ----------
    hours : int

    Returns
    -------
    dict
    """

    return _build_timeseries(hours)


# ==========================================================
# Internal Functions
# ==========================================================

def _traffic_profile(hour: int):
    """
    Simulate telecom daily traffic curve.
    """

    if 6 <= hour < 10:
        return 0.6

    elif 10 <= hour < 14:
        return 1.0

    elif 14 <= hour < 17:
        return 0.8

    elif 17 <= hour < 21:
        return 1.1

    else:
        return 0.3


def _node_profile(node: str):
    """
    Return engineering profile for
    a network function.
    """

    profiles = {

        "AMF": {
            "base_sessions": 22000,
            "cpu_multiplier": 55,
            "throughput_multiplier": 0.03
        },

        "SMF": {
            "base_sessions": 18000,
            "cpu_multiplier": 60,
            "throughput_multiplier": 0.025
        },

        "UPF": {
            "base_sessions": 15000,
            "cpu_multiplier": 65,
            "throughput_multiplier": 0.12
        },

        "PCF": {
            "base_sessions": 9000,
            "cpu_multiplier": 35,
            "throughput_multiplier": 0.015
        }
    }

    return profiles[node]


def _apply_noise():
    """
    Apply small variation to avoid
    identical KPI patterns.
    """

    return random.uniform(0.95, 1.05)


def _generate_node_metrics(
    node: str,
    traffic: float,
    noise: float
):
    """
    Generate correlated KPIs for a node.

    Traffic
        ↓
    Sessions
        ↓
    CPU
        ↓
    Memory
        ↓
    Latency
        ↓
    Throughput
    """

    profile = _node_profile(node)

    sessions = int(
        profile["base_sessions"]
        * traffic
        * noise
    )

    cpu = min(
        100,
        25
        + traffic
        * profile["cpu_multiplier"]
        * noise
    )

    memory = min(
        100,
        30
        + cpu * 0.75
        + random.uniform(-4, 4)
    )

    latency = (
        8
        + cpu * 0.20
        + random.uniform(-2, 2)
    )

    throughput = (
        sessions
        * profile["throughput_multiplier"]
    )
    # ##### Temporary
    # if node == "UPF":
    #     cpu = 99

    return {

        "cpu_usage": round(cpu, 2),

        "memory_usage": round(memory, 2),

        "sessions": sessions,

        "throughput_mbps": round(
            throughput,
            2
        ),

        "latency_ms": round(
            latency,
            2
        ),

        "traffic_factor": traffic
    }


def _build_snapshot(timestamp):
    """
    Build KPI snapshot for all nodes
    at a single point in time.
    """

    hour = timestamp.hour

    traffic = _traffic_profile(hour)

    snapshot = {}

    for node in NODES:

        metrics = _generate_node_metrics(
            node=node,
            traffic=traffic,
            noise=_apply_noise()
        )

        snapshot[node] = {

            "timestamp": timestamp.isoformat(),

            **metrics
        }

    return {

        "generated_at": datetime.utcnow().isoformat(),

        "nodes": snapshot
    }


def _build_timeseries(hours: int):
    """
    Generate KPI history.

    Returns KPI evolution across
    multiple timestamps.
    """

    base_time = datetime.utcnow() - timedelta(
        hours=hours
    )

    data = {
        node: []
        for node in NODES
    }

    for hour in range(hours):

        timestamp = (
            base_time
            + timedelta(hours=hour)
        )

        snapshot = _build_snapshot(timestamp)

        for node in NODES:

            data[node].append(
                snapshot["nodes"][node]
            )

    return {

        "generated_at": datetime.utcnow().isoformat(),

        "timeseries": data
    }

def generate_all_nodes():
    return generate_snapshot()