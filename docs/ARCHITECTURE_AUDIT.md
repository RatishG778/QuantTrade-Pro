# Architecture Audit

## Executive summary

QuantTrade-Pro is presently a Python-based quantitative research and backtesting application centered on a Streamlit dashboard and a set of research modules. It has a legitimate foundation for strategy experimentation, portfolio analytics, walk-forward studies, and Monte Carlo analysis, but it is not yet a production-grade trading infrastructure platform. The project is best understood as a research prototype and feature-rich notebook-style workflow that still needs a disciplined migration toward a modular backend, explicit risk controls, broker abstraction, and compliance-safe live trading gates.

The repository currently demonstrates useful research capability, but it lacks the backbone needed for regulated, multi-user, audit-friendly, and operationally safe trading infrastructure.

---

## Current architecture

### High-level structure

The project currently follows this pattern:

- Streamlit front end entry point in `app.py`
- Dashboard modules under `dashboard/`
- Quant logic under `core/` and `research/`
- Machine learning modules under `ml/`
- Data flows via local CSV/processed datasets and database-backed experiment storage
- Minimal event and workflow components under `core/workflow/` and `automation/`

### Observed technical stack

From the repository files and configuration, the current implementation is primarily:

- Python 3.11
- Pandas, NumPy, Plotly, Streamlit, TA-Lib-style indicators
- Custom backtesting engine classes
- SQLite-based research database and repository pattern
- Basic risk and position sizing logic
- Research modules for optimization, Monte Carlo, validation, reports, and portfolio analysis

### Key runtime entry point

- `app.py` launches a Streamlit app and routes into research and backtesting views.
- The app calls functions in `dashboard/run_backtest.py` and other dashboard modules.
- The current UI is strongly tied to research and strategy comparison rather than a true service-oriented platform.

---

## Working features observed

### Strategy and signal research

The repository contains a recognizable strategy engine with the following patterns:

- `core/strategies/base_strategy.py`
- `core/strategies/moving_average.py`
- `core/strategies/rsi_strategy.py`
- `core/strategies/macd_strategy.py`
- `core/strategies/strategy_factory.py`
- `core/strategies/signal_generator.py`

This shows the project already supports a modular strategy abstraction and strategy-based signal generation.

### Backtesting engine

The backtesting layer is present and partly functional:

- `core/backtesting/engine.py`
- `core/backtesting/portfolio.py`
- `core/backtesting/broker.py`
- `core/backtesting/metrics.py`
- `core/backtesting/result.py`
- `core/backtesting/analytics.py`

The engine simulates a basic flow of signal evaluation, portfolio buys/sells, and result generation. It includes a simple broker abstraction and portfolio accounting logic.

### Risk and position sizing

The risk system exists but is intentionally minimal:

- `core/risk/risk_manager.py`
- `core/risk/position_sizing.py`
- `core/risk/stop_loss.py`
- `core/risk/take_profit.py`

This is a useful starting point, but it is not yet a production-grade risk framework. It does not yet enforce comprehensive position limits, pre-trade checks, order blocking, or kill-switch coordination.

### Research and validation

The project includes substantial research functionality:

- Monte Carlo simulation under `research/monte_carlo/`
- Optimization logic under `research/optimization/`
- Walk-forward validation under `research/walk_forward/` and `research/validation/`
- Experiment repository and database under `research/database/`
- Reporting modules under `research/reports/`

This is one of the strongest areas of the current codebase and a clear migration asset.

### Portfolio analytics

Portfolio and analytics modules are present under:

- `core/portfolio_engine/`
- `dashboard/portfolio_dashboard.py`
- `dashboard/portfolio_metrics.py`
- `dashboard/performance.py`

This indicates a meaningful data-science / portfolio research foundation.

### Machine learning baseline

There are machine learning components under `ml/`, including model and dataset modules. They should be treated as research baselines rather than production trading intelligence.

---

## Broken, weak, or incomplete areas

### 1. The current platform is not service-based

There is no true backend, API layer, or worker ecosystem. The app is tightly coupled to the Streamlit UI and remains a monolith with research functions embedded directly in the dashboard flow.

### 2. Live trading is not meaningfully isolated

There is no explicit environment architecture for DEVELOPMENT / PAPER / LIVE. The repository does not implement a robust live-trading safety gate or explicit kill-switch architecture.

### 3. Risk controls are far too lightweight

The `RiskManager` currently checks only a single max-position condition. That is not enough for real-world portfolio risk checks, circuit breakers, stale-price protection, leverage limits, or order-frequency throttling.

### 4. Data quality validation is lacking

The repository does not show a first-class market data validation engine, instrument master, corporate action handling, or data quality scoring framework. This is a critical gap because invalid data can silently compromise backtests and live trading logic.

### 5. Broker abstraction is immature

There is a basic broker class, but no actual adapter model, no authentication architecture, no broker-specific integration layer, and no order reconciliation or broker-state sync logic.

### 6. Compliance and legal readiness are absent

There is no compliance module, no audit framework, no user-role matrix, and no regulated-live-trading review logic.

### 7. Security is underdeveloped

The codebase does not yet show:

- OIDC/OAuth-ready auth
- MFA architecture
- encrypted secrets management
- role-based access control
- audit log immutability
- rate limiting
- secure headers
- CSRF protections
- least-privilege database access

### 8. Data and schema architecture are not enterprise-ready

The project has research and local database patterns, but no verified PostgreSQL schema design, migration strategy, or multi-tenant data model. The project is not yet ready for real user isolation or enterprise-scale concurrency.

### 9. There is no production execution lifecycle

The repository does not implement a proper execution service with states such as `VALIDATED`, `RISK_APPROVED`, `SUBMITTED`, `ACKNOWLEDGED`, `PARTIALLY_FILLED`, `FILLED`, `REJECTED`, `CANCELLED`, and `FAILED` with reconciliation. The current backtesting engine is not equivalent to a live execution engine.

### 10. There is no paper-trading fidelity layer

Paper trading is not yet modeled as a realistic simulation of latency, partial fills, broker failures, spreads, fees, and order rejection. The current system is research-focused, not operationally realistic.

---

## Technical debt

### Architectural debt

- Dashboard logic is tightly coupled to core calculations.
- Strategy code is not clearly isolated from UI and execution concerns.
- No central domain model for instruments, orders, portfolios, or risk events.
- No versioned strategy registry or explicit reproducibility system beyond ad hoc research outputs.

### Data debt

- No explicit raw-vs-processed dataset policy beyond folders.
- No normalized market data contract.
- No canonical instrument master.
- No quality scoring for historical datasets.

### Engineering debt

- No service layer boundaries.
- No API versioning.
- No environment separation.
- No migration tooling.
- No audit trail for important changes and strategy activations.
- No formal observability stack or health checks.

---

## Security problems

The following are current concerns:

- Secrets are not obviously centralized or encrypted.
- There is no secure credential storage design for broker or API access.
- No role-based permissions have been identified.
- No explicit audit log protectiveness is implemented.
- No privacy or multi-tenancy controls are present.
- No commitment to non-plain-text storage of sensitive credentials.

This is a critical gap if the platform is ever extended toward live trading or brokerage integrations.

---

## Scalability problems

The current project is not designed for large-scale concurrency or production load:

- Streamlit is not the right runtime boundary for long-lived production workflows.
- Background workers, message queues, and task orchestration are absent.
- Large historical datasets should not be served directly through the front end.
- There is no async or event-driven route for live market data ingestion or order processing.
- No database design is in place for multi-user, multi-org workloads.

---

## Missing components relative to the target state

The following are absent or only partially present:

- FastAPI backend with OpenAPI schema and Pydantic models
- PostgreSQL with migrations
- Redis and worker queues
- Event bus / event-driven architecture
- Market data provider abstraction
- Instrument master and corp-action normalization
- Data validation and quality scoring engine
- Strategy versioning and strategy registry
- Broker adapter architecture and sandbox/UAT environment
- Reconciliation engine
- Risk engine with pre-trade checks, kill switch, and alerting
- Compliance module and legal review workflow
- Live trading readiness gate
- Multi-tenant SaaS model foundations
- Human-in-the-loop operational controls

---

## Migration plan

### Phase 1: Audit and stabilization

- Preserve working research modules.
- Document the existing strategy and backtesting capabilities.
- Identify which components will move into a backend domain model.
- Freeze the current codebase as a baseline for migration.

### Phase 2: Extract quant logic from the UI

- Move strategy logic, portfolio logic, and risk calculation into clean Python packages.
- Remove direct dependency on dashboard concerns.
- Standardize data contracts and strategy interfaces.

### Phase 3: Establish backend foundations

- Introduce FastAPI service layer.
- Add Pydantic schemas and domain models.
- Create identity and authorization boundaries.
- Build a structured repository pattern using PostgreSQL.

### Phase 4: Data and validation architecture

- Add market data provider abstraction.
- Standardize raw and processed datasets.
- Implement data quality checks.
- Introduce instrument master and market calendar definitions.

### Phase 5: Risk, execution, and paper trading

- Centralize risk enforcement.
- Create execution lifecycle tracking.
- Implement realistic paper-trading simulator.
- Add kill switches and order monitoring.

### Phase 6: Compliance and operational safety

- Create `compliance/` modules.
- Add user roles, audit log architecture, and legal review checkpoints.
- Enforce live-trading disablement unless readiness checks pass.

### Phase 7: Broker integration and reconciliation

- Add broker adapters and sandbox integrations.
- Add order reconciliation and alerting.
- Ensure live execution stays behind explicit controls.

### Phase 8: SaaS and scale preparation

- Introduce multi-tenant ownership patterns.
- Plan subscription tiers and permission boundaries.
- Set up observability, metrics, and operational monitoring.

---

## Conclusion

QuantTrade-Pro already contains a useful research engine and a promising strategy/backtesting foundation, but it is not yet a production-grade trading platform. The next phase must be methodical, with special attention to risk, auditability, compliance, and environment isolation. The core objective is not to “predict markets” but to build infrastructure that is reproducible, explainable, testable, and safe.

This project should evolve from a Streamlit-led research app into a modular trading operating system with explicit boundaries between research, execution, risk, and compliance.
