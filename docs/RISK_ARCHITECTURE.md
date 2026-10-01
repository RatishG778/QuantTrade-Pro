# Risk Architecture

## Risk philosophy

Risk is treated as a first-class system capability, not a secondary concern.

The platform must assume that every external dependency can fail, every data source can be imperfect, and every strategy can generate loss. The design objective is not to maximize aggressive execution; it is to preserve capital, maintain operational integrity, and provide clear auditability.

---

## Core principles

1. Capital protection comes before profit generation.
2. Live trading must never be enabled by default.
3. Every order must pass through centralized risk checks.
4. Risk controls must operate independently of strategy code.
5. All material risk events must be logged and reviewable.
6. The platform must fail safely and transparently.

---

## Risk architecture layers

### 1. Strategy layer

Strategy logic can generate signals, but strategy code must not directly place orders without passing through the risk and execution pipeline.

### 2. Risk validation layer

Before any order or trade action, the system must evaluate:

- position size
- portfolio exposure
- leverage
- drawdown limits
- daily loss thresholds
- strategy-level loss thresholds
- order value caps
- order frequency
- duplicate order protection
- stale price protection
- abnormal price detection
- market regime gating

### 3. Execution layer

The execution engine validates orders, checks the broker state, manages retries, and records lifecycle events while maintaining operational discipline.

### 4. Reconciliation layer

This layer compares internal accounting with broker/accounting states to detect missing, unknown, or inconsistent orders and positions.

### 5. Control and kill-switch layer

Global kill switches must be able to halt order flows regardless of strategy state. The platform should support:

- Global kill switch
- Strategy kill switch
- Account kill switch

---

## Required risk checks

### Pre-trade checks

- maximum position size
- maximum portfolio exposure
- maximum daily loss
- maximum strategy loss
- maximum order value
- maximum leverage
- maximum open positions
- maximum order frequency
- duplicate-order prevention
- stale-price protection
- abnormal-price protection
- circuit-breaker handling
- broker disconnect handling

### Real-time checks

- daily P&L versus limit
- open exposure versus policy
- broker connectivity status
- market status and session validity
- order state verification before retrial
- internal vs. broker state reconciliation

---

## Order approval flow

The design should follow this pattern:

Signal
↓
Risk Check
↓
Position Check
↓
Exposure Check
↓
Margin Check
↓
Loss Limit Check
↓
Order Validation
↓
Execution

This flow must be enforced centrally, not by ad hoc strategy-specific code.

---

## Kill-switch model

### Global kill switch

Stops all new orders and freezes live execution while preserving logs and important system state.

### Strategy kill switch

Stops a specific strategy while allowing other strategies or the wider portfolio to continue under policy.

### Account kill switch

Stops a specific account or broker connection when risk, operational, or connection conditions require it.

The kill switch must be independent of strategy code and must be reflected in audit records.

---

## Risk metrics to monitor

The system should monitor and display metrics including:

- portfolio VaR
- maximum drawdown
- current drawdown
- gross exposure
- net exposure
- leverage
- daily loss
- strategy risk
- concentration
- margin utilization
- order rejection rate
- fill quality and slippage

---

## Operational failure handling

Every external dependency must be treated as failure-prone.

The platform should define handling for:

- API timeout
- broker outage
- database outage
- Redis outage
- market-data outage
- network failure
- duplicate message
- stale data
- partial execution
- unknown order status

No silent fail states are acceptable. Risk controls and execution logic must surface operational issues clearly.

---

## Auditability requirements

Each risk event should be recorded with:

- timestamp
- user or system actor
- strategy ID or strategy version
- account or portfolio context
- order details
- decision outcome
- reason for denial or escalation

This allows forensic review and supports accountability.

---

## Assumed architecture direction

The final platform should contain:

- centralized risk policy configuration
- order validation before submission
- event-driven risk notifications
- reconciliation against external account state
- operational alerts for limit breaches and broker issues
- explicit no-go gates for live execution

---

## Risk conclusion

The repository’s current risk layer is too minimal for a production-grade trading infrastructure platform. The system needs a formal, centralized, policy-driven risk architecture that sits between strategy logic and execution, regardless of which strategy or broker is active.
