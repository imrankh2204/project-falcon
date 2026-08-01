"""
Project Falcon

FAL-540-R3

Runtime Lifecycle Validation

Validates the complete lifecycle of the paper trading runtime.

Validation Flow
---------------
PaperRuntimeFactory
        │
        ▼
LiveRuntime
        │
        ├── start()
        ├── process multiple events
        ├── stop()
        └── ignore events after shutdown
"""

from __future__ import annotations

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
    Minimal strategy used for lifecycle validation.
    """

    def evaluate(
        self,
        event,
    ):
        #
        # No trades required for lifecycle validation.
        #
        return {}


class MockEventSource:
    """
    Minimal event source.
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

    strategy_engine = (
        MockStrategyEngine()
    )

    signal_translator = (
        TradeSignalTranslator()
    )

    risk_manager = (
        RiskManager()
    )

    event_source = (
        MockEventSource()
    )

    runtime = (
        PaperRuntimeFactory().create(
            strategy_engine=strategy_engine,
            signal_translator=signal_translator,
            risk_manager=risk_manager,
            event_source=event_source,
        )
    )

    print(
        "PASS: Runtime created"
    )

    #
    # Start runtime.
    #
    runtime.start()

    assert runtime.running is True

    assert event_source.started is True

    print(
        "PASS: Runtime started"
    )

    #
    # Process multiple deterministic events.
    #
    for price in (
        25000,
        25010,
        25025,
    ):

        runtime.process_event(
            {
                "symbol": "NIFTY",
                "price": price,
            }
        )

    assert runtime.running is True

    print(
        "PASS: Multiple events processed"
    )

    #
    # Stop runtime.
    #
    runtime.stop()

    assert runtime.running is False

    assert event_source.stopped is True

    print(
        "PASS: Runtime stopped"
    )

    #
    # Events after shutdown should be ignored.
    #
    result = runtime.process_event(
        {
            "symbol": "NIFTY",
            "price": 25100,
        }
    )

    assert result is None

    print(
        "PASS: Events ignored after shutdown"
    )

    print()

    print(
        "FAL-540-R3 COMPLETE"
    )


if __name__ == "__main__":
    main()