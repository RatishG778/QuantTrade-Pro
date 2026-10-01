# Technical Roadmap

## Current state

The repository is currently a research-oriented Python trading app with the following principal characteristics:

- Streamlit dashboard for research and backtesting
- modular strategy classes and signal generation
- portfolio and results objects for basic backtests
- optimization, validation, and Monte Carlo research modules
- experiment tracking and research database patterns
- no production backend, governance layer, or compliance architecture

---

## Phase 1: Audit and stabilization

### Objective

Preserve the working research assets while identifying the components that must be extracted into service-oriented modules.

### Deliverables

- architecture audit
- migration notes
- risk and compliance baseline
- repository inventory and ownership map

### Success criteria

- existing strategy and research logic is documented
- key risks and gaps are mapped
- no major functionality is lost during migration

---

## Phase 2: Domain extraction and architecture cleanup

### Objective

Move quantitative logic out of UI dependencies and into reusable Python packages.

### Planned work

- isolate strategy definitions from Streamlit
- standardize strategy interfaces
- separate portfolio math from display code
- create domain models for orders, fills, positions, and accounts
- normalize the backtesting engine around an event-driven flow

### Success criteria

- dashboard code depends on domain services rather than inlined calculations
- strategy can run in multiple environments without UI changes
- portfolio behavior can be tested outside the dashboard

---

## Phase 3: Backend and API foundation

### Objective

Build a backend platform that supports research workflows and operational processing.

### Planned work

- FastAPI application with versioned endpoints
- Pydantic schemas for validation and contracts
- SQLAlchemy or a disciplined repository layer on PostgreSQL
- basic auth and RBAC foundations
- service-oriented modules for strategy, portfolio, risk, and execution

### Success criteria

- strategies and backtests can be created through APIs
- auth and authorization boundaries are explicit
- DB schema updates happen through migrations rather than ad hoc edits

---

## Phase 4: Data and market-data architecture

### Objective

Create a robust market-data abstraction and data quality framework.

### Planned work

- `MarketDataProvider` abstraction
- CSV, DB, broker, and licensed provider variants
- instrument master record model
- data quality checks and reporting
- handling of corporate actions, trading holidays, and stale data

### Success criteria

- historical data is validated before use
- dataset corruption cannot silently propagate into backtests
- providers are interchangeable without strategy rewrites

---

## Phase 5: Risk engine and execution lifecycle

### Objective

Create the protective core of the platform.

### Planned work

- centralized `RiskEngine`
- policy definitions for exposure, leverage, daily loss, and order size
- kill switches at global, strategy, and account levels
- execution lifecycle state tracking
- duplicate-order prevention and reconciliation

### Success criteria

- no order reaches execution without required checks
- the platform can block live operations safely and consistently
- execution events are auditable and reproducible

---

## Phase 6: Paper trading and realistic simulation

### Objective

Provide a system that behaves close to live trading without actual brokerage execution.

### Planned work

- realistic slippage and spread simulation
- partial fills and latency modeling
- market-session and order rejection behavior
- broker-like lifecycle events
- order reconciliation simulation

### Success criteria

- strategy behavior in paper mode reflects realistic operational friction
- live and paper environments remain separate and distinct

---

## Phase 7: Broker abstraction and sandbox integrations

### Objective

Prepare for controlled broker communication without exposing unsafe live execution paths.

### Planned work

- `BrokerAdapter` interface
- broker-specific adapters
- sandbox/UAT modes
- authentication and token safe handling
- reconciliation between internal orders and broker state

### Success criteria

- broker code is centralized and isolated
- live execution remains disabled until all checks pass
- unknown order states are treated as operational issues, never silently retried

---

## Phase 8: Compliance, security, and audit

### Objective

Create the governance layer required for serious trading infrastructure.

### Planned work

- `compliance/` module
- legal/compliance checklist and review gates
- audit logs for orders, strategy changes, and risk events
- RBAC and secure secret storage
- monitoring, health checks, and operational alerting

### Success criteria

- all material actions are logged
- secrets are never stored in plain text
- live trading remains disabled without documented readiness

---

## Phase 9: Research platform enhancements

### Objective

Advance the quantitative research experience without breaking rigor.

### Planned work

- strategy versioning and reproducibility
- strategy lab and experiment comparison workspace
- walk-forward and out-of-sample formalization
- Monte Carlo risk distribution reporting
- benchmark analysis and attribution

### Success criteria

- research outputs are traceable to datasets and versions
- in-sample and out-of-sample results are reported distinctly
- results are explainable and not overfit by default

---

## Phase 10: Live-trading readiness gate

### Objective

Create a formal go/no-go gate before any live execution.

### Required gate checks

- firm data-source validation
- broker connection readiness
- authentication and authorization controls
- configured risk limits
- kill-switch architecture
- order reconciliation readiness
- audit logging readiness
- paper-trading validation
- strategy validation and regression behavior
- compliance review status

### Success criteria

- live mode is disabled by default
- enabling live mode requires explicit controls and approvals
- no live execution can occur from development code paths

---

## Long-term target architecture

The end-state should resemble:

- frontend: modern, institutional dashboard
- backend: FastAPI + service modules
- data layer: PostgreSQL, Redis, object storage, queueing
- quant layer: strategy engine, portfolio engine, risk engine, execution engine
- broker layer: adapter-based integration with sandbox and live modes
- observability: dashboards, health checks, metrics, error tracking, audit logs

---

## Deliverable expectation

The product should evolve toward a disciplined trading infrastructure company structure, not a portfolio of disconnected scripts. The roadmap is intentionally risk-first and operationally conservative.
