"""
===========================================================
Scenario Store
===========================================================

Purpose
-------
Centralized scenario management service used to inject
telecom anomalies into the KPI generation pipeline.

The Scenario Store enables controlled simulation of
Packet Core incidents for:

- Dashboard demonstrations
- RCA (Root Cause Analysis) validation
- AI Copilot testing
- NOC training
- Executive reporting scenarios
- Time-series anomaly visualization

Supported Functions
-------------------
The module allows:

1. Scenario Registration
   Define anomaly templates affecting AMF, SMF,
   UPF, PCF, or future network functions.

2. Scenario Activation
   Enable scenarios dynamically from the dashboard
   without modifying code.

3. Scenario Deactivation
   Remove injected anomalies and restore normal KPI
   generation.

4. Multiple Concurrent Scenarios
   Run several scenarios simultaneously to simulate
   realistic outage conditions.

5. KPI Overrides
   Inject synthetic values for:

   - CPU Usage
   - Memory Usage
   - Session Count
   - Throughput
   - Latency
   - Registration Rate
   - PFCP Failures
   - GTP-U Drops

6. Copilot Integration
   Expose active scenarios to AI Copilot so generated
   insights and RCA reports are aware of synthetic
   network conditions.

7. Time-series Event Markers
   Provide scenario metadata to annotate dashboard
   charts and anomaly timelines.

Architecture
------------
Dashboard
    │
    ▼
Scenario API
    │
    ▼
Scenario Manager
    │
    ▼
KPI Generator
    │
    ▼
Time Series Database
    │
    ▼
Dashboard / Copilot

Usage
-----

Activate Scenario

    activate_scenario(
        "upf_congestion"
    )

Deactivate Scenario

    deactivate_scenario(
        "upf_congestion"
    )

Get Active Scenarios

    get_active_scenarios()

Apply Scenario Overrides

    metrics = apply_scenarios(
        "UPF",
        metrics
    )

Example
-------

Normal KPI

    {
        "cpu_usage": 62,
        "memory_usage": 55,
        "latency_ms": 12
    }

Active Scenario

    upf_congestion

Result

    {
        "cpu_usage": 95,
        "memory_usage": 98,
        "latency_ms": 120
    }

Scenario Lifecycle
------------------

NORMAL
   │
   ▼
ACTIVATED
   │
   ▼
INJECT KPI OVERRIDES
   │
   ▼
MARK TIME SERIES
   │
   ▼
COPILOT RCA
   │
   ▼
DEACTIVATED

Author
------
Packet Core AI Operations Platform

Version
-------
2.0
===========================================================
"""

"""
===========================================================
Scenario Store
===========================================================
"""

from datetime import datetime

ACTIVE_SCENARIOS = []


SCENARIOS = {

    "upf_congestion": {
        "severity": "critical",
        "description": "UPF resource congestion",
        "affected_nodes": ["UPF"],
        "overrides": {
            "UPF": {
                "cpu_usage": 95,
                "memory_usage": 98,
                "latency_ms": 120
            }
        }
    },

    "session_storm": {
        "severity": "critical",
        "description": "Massive signaling surge",
        "affected_nodes": ["AMF", "SMF"],
        "overrides": {
            "AMF": {
                "sessions": 100000
            },
            "SMF": {
                "sessions": 80000
            }
        }
    },

    "memory_leak": {
        "severity": "high",
        "description": "SMF memory exhaustion",
        "affected_nodes": ["SMF"],
        "overrides": {
            "SMF": {
                "memory_usage": 99
            }
        }
    },

    "latency_degradation": {
        "severity": "high",
        "description": "Data plane latency spike",
        "affected_nodes": ["UPF"],
        "overrides": {
            "UPF": {
                "latency_ms": 250
            }
        }
    },

    "smf_overload": {
        "severity": "critical",
        "description": "SMF overload",
        "affected_nodes": ["SMF"],
        "overrides": {
            "SMF": {
                "cpu_usage": 95,
                "memory_usage": 97,
                "sessions": 90000
            }
        }
    },

    "amf_registration_storm": {
        "severity": "critical",
        "description": "Registration storm",
        "affected_nodes": ["AMF"],
        "overrides": {
            "AMF": {
                "cpu_usage": 95,
                "sessions": 150000
            }
        }
    }
}