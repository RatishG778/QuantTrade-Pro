"""Broker requirements and integration checklist placeholders.

This file intentionally avoids making legal claims. It records requirements that
must be validated before a broker integration is used in live trading.
"""

from __future__ import annotations

BROKER_INTEGRATION_REQUIREMENTS = [
    "Broker API contract and permissions reviewed",
    "Authentication and token storage reviewed",
    "Sandbox/UAT access and testing validated",
    "Account segregation and permissions verified",
    "Order lifecycle and reconciliation tested",
    "Risk policy and kill-switch design reviewed",
    "Network, IP, and session controls reviewed",
    "Audit log capture confirmed",
    "REQUIRES LEGAL/COMPLIANCE REVIEW: broker-specific regulatory obligations",
]


def broker_requirements_summary() -> list[str]:
    return BROKER_INTEGRATION_REQUIREMENTS[:]
