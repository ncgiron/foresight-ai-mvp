"""
===========================================================
Telecom Network Topology

Purpose
-------
Represents the dependency relationships between
Packet Core Network Functions.

This will later support:

- Root Cause Analysis
- Impact Assessment
- Correlation Engine
- AI Investigations
===========================================================
"""

TOPOLOGY = {

    # AMF controls device registration
    "AMF": ["SMF"],

    # SMF manages PDU sessions
    "SMF": ["UPF"],

    # UPF handles user-plane traffic
    "UPF": [],

    # PCF provides policy control
    "PCF": ["SMF"]
}