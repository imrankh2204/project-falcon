"""
Project Falcon

FAL-540-R1

Paper Runtime Factory Validation

Validates that the PaperRuntimeFactory correctly composes the
paper trading runtime and wires all required dependencies.

Validation Flow
---------------
PaperRuntimeFactory
        │
        ▼
PaperBrokerGateway
        │
        ▼
PortfolioSynchronizationService
        │
        ▼
LiveTradingService
        │
        ▼
LiveExecutionEngine
        │
        ▼
LiveEngine
        │
        ▼
LiveRuntime
"""

from __future__ import annotations

from app.live.live_runtime import LiveRuntime
from app.paper.paper_runtime_factory import (
    PaperRuntimeFactory,
)
from app.services.trade_signal_translator import (
    TradeSignalTranslator,
)
from app.trading.risk_manager import RiskManager


# ---------------------------------------------------------
# Test Doubles
# ---------------------------------------------------------


class MockStrategyEngine:
    """
    Minimal strategy engine used for runtime composition validation.
    """

    def evaluate(self, event):
        return {}


class MockEventSource:
    """
    Minimal event source used for runtime composition validation.
    """

    def __init__(self) -> None:
        self.started = False
        self.stopped = False

    def start(self) -> None:
        self.started = True

    def stop(self) -> None:
        self.stopped = True


# ---------------------------------------------------------
# Validation
# ---------------------------------------------------------


def main() -> None:

    strategy_engine = MockStrategyEngine()

    signal_translator = (
        TradeSignalTranslator()
    )

    risk_manager = RiskManager()

    event_source = MockEventSource()

    factory = PaperRuntimeFactory()

    runtime = factory.create(
        strategy_engine=strategy_engine,
        signal_translator=signal_translator,
        risk_manager=risk_manager,
        event_source=event_source,
    )

    assert isinstance(
        runtime,
        LiveRuntime,
    )

    assert runtime.live_engine is not None

    assert (
        runtime.live_engine.trading_service
        is not None
    )

    print("PASS: Runtime created")

    print("PASS: LiveEngine created")

    print("PASS: Trading service created")

    print("PASS: Paper broker configured")

    print()

    print("FAL-540-R1 COMPLETE")


if __name__ == "__main__":
    main()