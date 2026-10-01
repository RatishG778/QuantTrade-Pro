"""Risk-control placeholders for future operational enforcement.

This module documents the minimum guardrails needed before live operations.
"""

from __future__ import annotations

RISK_CONTROL_REQUIREMENTS = [
    "Maximum position size limits",
    "Maximum portfolio exposure limits",
    "Maximum daily loss limits",
    "Maximum strategy loss limits",
    "Maximum order value limits",
    "Leverage controls",
    "Open-position limits",
    "Order-frequency throttling",
    "Duplicate-order prevention",
    "Stale-price protection",
    "Abnormal-price protection",
    "Circuit-breaker handling",
    "Broker disconnect handling",
    "Audit logging for all risk decisions",
]


def risk_control_summary() -> list[str]:
    return RISK_CONTROL_REQUIREMENTS[:]
