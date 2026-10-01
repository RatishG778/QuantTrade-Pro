"""Structured compliance checklist and readiness markers.

The project must never treat live-broker connectivity as evidence of legal or
operational readiness.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class ComplianceCheck:
    name: str
    status: str = "PENDING"
    notes: str = ""


@dataclass
class LiveTradingReadiness:
    data_source: str = "PENDING"
    broker_connection: str = "PENDING"
    authentication: str = "PENDING"
    risk_limits: str = "PENDING"
    kill_switch: str = "PENDING"
    order_reconciliation: str = "PENDING"
    audit_logging: str = "PENDING"
    paper_trading: str = "PENDING"
    strategy_validation: str = "PENDING"
    compliance_review: str = "PENDING"

    def to_dict(self) -> Dict[str, str]:
        return {
            "Data Source": self.data_source,
            "Broker Connection": self.broker_connection,
            "Authentication": self.authentication,
            "Risk Limits": self.risk_limits,
            "Kill Switch": self.kill_switch,
            "Order Reconciliation": self.order_reconciliation,
            "Audit Logging": self.audit_logging,
            "Paper Trading": self.paper_trading,
            "Strategy Validation": self.strategy_validation,
            "Compliance Review": self.compliance_review,
        }


REQUIRED_CHECKS: List[ComplianceCheck] = [
    ComplianceCheck("SEBI and exchange requirements review", "PENDING", "REQUIRES LEGAL/COMPLIANCE REVIEW"),
    ComplianceCheck("Broker onboarding and contract review", "PENDING", "REQUIRES LEGAL/COMPLIANCE REVIEW"),
    ComplianceCheck("Algo registration and operational review", "PENDING", "REQUIRES LEGAL/COMPLIANCE REVIEW"),
    ComplianceCheck("Data licensing review", "PENDING", "REQUIRES LEGAL/COMPLIANCE REVIEW"),
    ComplianceCheck("Audit log retention and evidence controls", "PENDING", "REQUIRES LEGAL/COMPLIANCE REVIEW"),
    ComplianceCheck("User consent and disclosures", "PENDING", "REQUIRES LEGAL/COMPLIANCE REVIEW"),
]


def live_trading_status() -> LiveTradingReadiness:
    """Returns an explicit live-trading readiness snapshot.

    The live environment remains disabled until each required control is explicitly
    validated and the compliance review is complete.
    """
    return LiveTradingReadiness()
