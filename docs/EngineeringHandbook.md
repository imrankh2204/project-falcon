Project Falcon
Project Goal

Project Falcon is a production-quality automated trading platform for Indian options trading.

Current scope:

Zerodha Kite Connect
NIFTY options
SENSEX options

Future scope:

BANKNIFTY
FINNIFTY
MIDCPNIFTY
Multiple brokers

The project is intentionally designed to become broker-neutral before additional brokers are added.

Development Philosophy

Every component is built according to the following principles.

Clean Architecture

Business rules never depend on:

Zerodha SDK
external APIs
persistence
UI

Only adapters depend on SDKs.

SOLID

Strict adherence.

Especially:

Single Responsibility
Dependency Inversion
Interface segregation
Immutable domain models

Every domain object is frozen.

Typical example:

@dataclass(frozen=True, slots=True)

Mutable state is isolated into services/managers.

Broker Neutrality

All broker-specific logic remains inside adapters.

Never leak:

KiteConnect
KiteTicker
Zerodha JSON
SDK constants

outside the broker layer.

Strong Typing

Entire repository uses:

from __future__ import annotations

Strict type hints everywhere.

Validation

Objects validate themselves.

Invalid state is rejected immediately.

Test Driven

Every milestone contains dedicated unit tests.

Repository Structure

High-level architecture:

Configuration

Broker

Market Domain

Historical Data

Replay Engine

Indicators

Strategy

Trading

Portfolio

Analytics

Backtesting

Paper Runtime

Live Runtime

Broker Session

Future:
Broker Profile
Order Routing
Execution
Risk
Development Workflow

Mandatory workflow established throughout the project:

Inspect repository
Review implementation
Design Review
Generate complete replacement files only
User runs
python -m compileall app
pytest
Architecture Review
Recommend Git checkpoint
Continue

No partial snippets.

No piecemeal patches.

Always full file replacements.

Major Completed Architecture
FAL-010

Configuration layer

BrokerConfig
Environment loader
Validation

Status:

Stable.

FAL-020

Broker abstraction.

Initial Kite wrapper.

No SDK leakage.

FAL-030

Market domain.

Immutable:

Instrument

OHLCV/Candle

Market structures.

FAL-040

Historical Market Data.

CSV Provider.

Historical abstraction.

FAL-050

Indicators.

Indicator engine.

Moving averages.

Extensible architecture.

FAL-060

Strategy engine.

Higher timeframe analysis.

Lower timeframe execution.

Current intended execution:

4H
1H
30m
15m

↓

5m
3m
1m
FAL-070

Trading Domain.

Major objects:

TradeRequest

Position

ExecutionUpdate

Portfolio

RiskManager

PaperExecutionEngine

TradingService

Architecture locked.

FAL-080

Trading lifecycle.

Complete entry/exit flow.

Portfolio integration.

Trading service orchestration.

FAL-090

Accounting.

Position accounting.

Portfolio accounting.

FAL-100

Portfolio Analytics.

Metrics include:

Win rate

Average winner

Average loser

Profit factor

Expectancy

FAL-110

Historical Provider

CSV implementation.

FAL-120

Replay Clock

Deterministic replay clock.

FAL-130

Replay Engine

ReplayEvent abstraction.

Sequential replay.

FAL-140

Backtest Session

Coordinates:

Replay

Strategy

Trading

Portfolio

Results

FAL-150

Strategy Replay Integration

Strategy consumes replay events.

Backtesting becomes deterministic.

Reporting

Implemented:

BacktestReport

CSV export

JSON export

Console output

Report builder

Exporter architecture

Performance Metrics

PerformanceSnapshot

PerformanceMetrics

BacktestResult

Immutable statistics.

Live Runtime

Architecture evolved significantly.

Current design:

MarketFeed

↓

LiveRuntime

↓

LiveEngine

↓

Trading Pipeline
Market Feed

Introduced:

MarketFeed protocol.

Future adapters:

Replay

Zerodha WebSocket

Future brokers

ReplayMarketFeed

Adapter allowing replay engine to behave as live market feed.

Important because:

Runtime does not know replay vs live.

Runtime Statistics

Implemented.

Captures runtime metrics.

Paper Runtime Factory

Factory builds:

PaperBrokerGateway

LiveTradingService

LiveRuntime

Automatically wires dependencies.

Live Runtime Integration

Earlier:

event_source

Later changed to:

market_feed

This unified replay and live execution.

Live Runtime Documentation

Added architecture documentation.

Broker Authentication Architecture

Latest completed subsystem.

Architecture:

BrokerConfig

↓

KiteClient

↓

AuthenticationService

↓

BrokerSession

↓

BrokerSessionManager

↓

BrokerSessionValidator

This architecture is considered validated and locked.

BrokerConfig

Responsible for:

API key

Secret

Broker settings

Validation

No runtime logic.

KiteClient

Thin SDK wrapper.

Responsibilities:

SDK initialization

API forwarding

No business logic.

AuthenticationService

Responsible only for authentication.

Expected responsibilities:

Login URL

Exchange request token

Generate access token

Fetch authenticated session

No validation logic.

No session persistence.

BrokerSession

Immutable representation of authenticated broker session.

No SDK objects.

Only broker-neutral fields.

BrokerSessionManager

Responsible for lifecycle.

Likely responsibilities:

Current session

Refresh

Invalidate

Replace

Single source of truth.

BrokerSessionValidator

Validates session health.

Checks include:

Authenticated

Required fields

Token validity

Broker-neutral validation.

Upcoming Milestone

FAL-714-R1

Broker Profile Domain.

Deliverables:

app/broker/broker_profile.py

app/broker/broker_profile_service.py

tests/broker/test_broker_profile.py

tests/broker/test_broker_profile_service.py

Requirements:

Immutable BrokerProfile.

Broker-neutral.

Reuse KiteClient.

Map Zerodha response only inside service.

Engineering Rules

Never:

Expose SDK types.

Return Zerodha JSON.

Pass KiteConnect outside adapter.

Always:

Return domain models.

Coding Style

Repository conventions:

__future__.annotations

@dataclass(frozen=True)

slots=True

typing

Protocols

Small classes

Single responsibility

No giant utility modules.

No static helper dumping grounds.

Testing Philosophy

Every milestone:

Compile:

python -m compileall app

Then:

pytest

Architecture review only after green validation.

Repository Validation Status

Latest validated checkpoint:

Repository:

imrankh2204/project-falcon

Branch:

main

HEAD:

a30c810

Validated milestone:

FAL-713-R3
Broker Session Validator

Validation:

python -m compileall app

PASS

pytest

40 tests passing
Git Workflow

After every validated milestone:

Create commit.

Recommend tag.

Continue.

No multiple milestones before validation.

Architecture Principles Established During the Project

These are considered architectural decisions unless a genuine design flaw is discovered:

Broker neutrality is mandatory.
Domain models are immutable.
Services own mutable behavior.
SDKs are confined to broker adapters.
Replay and live runtimes share the same execution pipeline through MarketFeed.
PaperRuntimeFactory composes runtime dependencies.
Runtime orchestration is deterministic and testable.
Business logic must remain independent of infrastructure concerns.
Complete file replacements are preferred over partial edits during milestone implementation.
Resolved Issues and Bugs

Throughout development, several issues were identified and resolved:

Early project setup
Fixed ImportError involving configuration loading.
Corrected a SyntaxError caused by erroneous content in app/__init__.py.
Standardized Python environment setup and activation.
Improved project scaffolding (.gitignore, .env.example, documentation, scripts).
Git and GitHub
Migrated from master to main.
Resolved GitHub authentication issues by switching from password authentication to SSH.
Verified SSH connectivity for repository operations.
Runtime and Architecture
Replaced event_source with market_feed in LiveRuntime, simplifying runtime architecture and unifying replay/live execution.
Introduced ReplayMarketFeed adapter to remove replay-specific runtime logic.
Added PaperRuntimeFactory to centralize dependency wiring.
Added runtime statistics support.
Trading and Backtesting
Completed deterministic replay pipeline.
Integrated strategy evaluation with replay events.
Stabilized trading lifecycle, accounting, analytics, and reporting.
Current Known Issues

Based on the latest validated checkpoint, there are no known functional bugs. The reported state is:

python -m compileall app ✔
pytest ✔ (40 tests passing)

The remaining work is planned feature development rather than bug fixing.

One operational limitation encountered during AI-assisted development was that repository inspection through GitHub was not available in the current chat session. Consequently, implementation work that explicitly required inspecting the live repository could not be performed without either repository access or the relevant source files.

Immediate Next Milestone

Proceed with FAL-714-R1 — Broker Profile Domain.

Objectives:

Add immutable BrokerProfile domain model.
Implement BrokerProfileService that retrieves profile information via the existing KiteClient.
Keep all Zerodha response mapping inside BrokerProfileService.
Add comprehensive unit tests.
Validate with:
python -m compileall app
pytest
Perform an architecture review.
Recommend a Git checkpoint before continuing.

This summary captures the project's architecture, design rationale, implementation progress, workflow, and current state, providing sufficient context for another AI assistant to resume development from the validated checkpoint without re-establishing prior decisions.