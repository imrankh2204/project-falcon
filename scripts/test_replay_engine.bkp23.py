"""
ReplayEngine validation tests.

This module validates the replay infrastructure composition
behavior of Project Falcon.

Validation coverage:

- Dependency injection
- Constructor validation
- Provider exposure
- Replay clock exposure
- Dependency identity preservation

The tests intentionally avoid replay execution logic because
ReplayEngine does not own replay iteration responsibilities.
"""

from __future__ import annotations

from datetime import datetime

from app.backtest.replay_engine import ReplayEngine
from app.backtest.replay_clock import ReplayClock
from app.backtest.historical_provider import HistoricalDataProvider


class DummyHistoricalProvider(HistoricalDataProvider):
    """
    Minimal test implementation of HistoricalDataProvider.

    Used only to validate ReplayEngine dependency injection.
    """

    def candles(self):
        """
        Return an empty candle iterator.

        ReplayEngine does not consume candles in the current
        architecture revision.
        """

        return iter(())


def test_replay_engine_initializes_with_valid_dependencies() -> None:
    """
    Validate successful ReplayEngine construction.
    """

    provider = DummyHistoricalProvider()

    clock = ReplayClock(
        datetime(
            2026,
            1,
            1,
            9,
            15,
        )
    )

    engine = ReplayEngine(
        provider,
        clock,
    )

    assert engine.provider is provider
    assert engine.clock is clock


def test_replay_engine_exposes_provider_reference() -> None:
    """
    Validate provider property exposure.
    """

    provider = DummyHistoricalProvider()

    clock = ReplayClock(
        datetime(
            2026,
            1,
            1,
            9,
            15,
        )
    )

    engine = ReplayEngine(
        provider,
        clock,
    )

    assert engine.provider == provider


def test_replay_engine_exposes_clock_reference() -> None:
    """
    Validate clock property exposure.
    """

    provider = DummyHistoricalProvider()

    clock = ReplayClock(
        datetime(
            2026,
            1,
            1,
            9,
            15,
        )
    )

    engine = ReplayEngine(
        provider,
        clock,
    )

    assert engine.clock == clock


def test_replay_engine_rejects_invalid_provider() -> None:
    """
    Validate provider dependency type checking.
    """

    clock = ReplayClock(
        datetime(
            2026,
            1,
            1,
            9,
            15,
        )
    )

    try:
        ReplayEngine(
            "invalid_provider",  # type: ignore[arg-type]
            clock,
        )

    except TypeError:
        return

    raise AssertionError(
        "Expected TypeError for invalid provider."
    )


def test_replay_engine_rejects_invalid_clock() -> None:
    """
    Validate clock dependency type checking.
    """

    provider = DummyHistoricalProvider()

    try:
        ReplayEngine(
            provider,
            "invalid_clock",  # type: ignore[arg-type]
        )

    except TypeError:
        return

    raise AssertionError(
        "Expected TypeError for invalid clock."
    )


def test_replay_engine_preserves_dependency_identity() -> None:
    """
    Validate injected dependencies are not copied or replaced.

    ReplayEngine should maintain references to the original
    provider and clock instances.
    """

    provider = DummyHistoricalProvider()

    clock = ReplayClock(
        datetime(
            2026,
            1,
            1,
            9,
            15,
        )
    )

    engine = ReplayEngine(
        provider,
        clock,
    )

    assert id(engine.provider) == id(provider)
    assert id(engine.clock) == id(clock)


def run_tests() -> None:
    """
    Execute all ReplayEngine validation tests.

    Provides a lightweight executable validation flow
    without external testing dependencies.
    """

    tests = [
        test_replay_engine_initializes_with_valid_dependencies,
        test_replay_engine_exposes_provider_reference,
        test_replay_engine_exposes_clock_reference,
        test_replay_engine_rejects_invalid_provider,
        test_replay_engine_rejects_invalid_clock,
        test_replay_engine_preserves_dependency_identity,
    ]

    for test in tests:
        test()
        print(f"PASSED: {test.__name__}")


if __name__ == "__main__":
    run_tests()