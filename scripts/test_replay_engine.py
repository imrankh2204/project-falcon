"""
ReplayEngine validation tests.

This module validates Project Falcon replay infrastructure.

Validation coverage:

Infrastructure:
    - Dependency injection
    - Dependency validation
    - Property exposure
    - Identity preservation

Replay execution:
    - ReplayEvent emission
    - ReplayClock synchronization
    - Candle propagation
    - Chronological replay ordering
    - Empty dataset behavior

The tests intentionally avoid strategy and execution logic
because ReplayEngine does not own those responsibilities.
"""

from __future__ import annotations

from collections.abc import Iterator
from datetime import datetime

from app.backtest.historical_provider import HistoricalDataProvider
from app.backtest.replay_clock import ReplayClock
from app.backtest.replay_engine import ReplayEngine
from app.backtest.replay_event import ReplayEvent
from app.market.candle import Candle
from app.market.timeframe import TimeFrame


class DummyHistoricalProvider(HistoricalDataProvider):
    """
    Minimal in-memory historical provider for validation.

    Provides deterministic candle iteration without
    filesystem or external data dependencies.
    """

    def __init__(
        self,
        candles: tuple[Candle, ...] = (),
    ) -> None:
        """
        Initialize provider with predefined candles.

        Parameters
        ----------
        candles:
            Immutable candle collection.
        """

        self._candles = candles

    def candles(self) -> Iterator[Candle]:
        """
        Return candle iterator.
        """

        return iter(self._candles)


def create_candle(
    timestamp: datetime,
    close: float,
) -> Candle:
    """
    Create deterministic test candle.

    Parameters
    ----------
    timestamp:
        Candle timestamp.

    close:
        Closing price.

    Returns
    -------
    Candle
        Test candle instance.
    """

    return Candle(
        timestamp=timestamp,
        open=100.0,
        high=105.0,
        low=95.0,
        close=close,
        volume=1000,
        timeframe=TimeFrame.ONE_MINUTE,
    )


def create_engine(
    candles: tuple[Candle, ...],
) -> ReplayEngine:
    """
    Create ReplayEngine test instance.
    """

    provider = DummyHistoricalProvider(candles)

    clock = ReplayClock(
        candles[0].timestamp
        if candles
        else datetime(
            2026,
            1,
            1,
            9,
            15,
        )
    )

    return ReplayEngine(
        provider,
        clock,
    )


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

    engine = ReplayEngine(
        provider,
        ReplayClock(
            datetime(
                2026,
                1,
                1,
                9,
                15,
            )
        ),
    )

    assert engine.provider is provider


def test_replay_engine_exposes_clock_reference() -> None:
    """
    Validate clock property exposure.
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

    engine = ReplayEngine(
        DummyHistoricalProvider(),
        clock,
    )

    assert engine.clock is clock


def test_replay_engine_rejects_invalid_provider() -> None:
    """
    Validate provider dependency validation.
    """

    try:
        ReplayEngine(
            "invalid_provider",  # type: ignore[arg-type]
            ReplayClock(
                datetime(
                    2026,
                    1,
                    1,
                    9,
                    15,
                )
            ),
        )

    except TypeError:
        return

    raise AssertionError(
        "Expected TypeError for invalid provider."
    )


def test_replay_engine_rejects_invalid_clock() -> None:
    """
    Validate clock dependency validation.
    """

    try:
        ReplayEngine(
            DummyHistoricalProvider(),
            "invalid_clock",  # type: ignore[arg-type]
        )

    except TypeError:
        return

    raise AssertionError(
        "Expected TypeError for invalid clock."
    )


def test_replay_engine_preserves_dependency_identity() -> None:
    """
    Validate dependency identity preservation.
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


def test_replay_engine_emits_replay_events() -> None:
    """
    Validate ReplayEvent generation.
    """

    candle = create_candle(
        datetime(
            2026,
            1,
            1,
            9,
            16,
        ),
        102.0,
    )

    engine = create_engine(
        (candle,),
    )

    events = list(engine.replay())

    assert len(events) == 1
    assert isinstance(
        events[0],
        ReplayEvent,
    )


def test_replay_engine_advances_clock_to_candle_time() -> None:
    """
    Validate ReplayClock synchronization.
    """

    timestamp = datetime(
        2026,
        1,
        1,
        9,
        16,
    )

    engine = create_engine(
        (
            create_candle(
                timestamp,
                102.0,
            ),
        ),
    )

    list(engine.replay())

    assert engine.clock.current_time == timestamp


def test_replay_engine_preserves_candle_identity() -> None:
    """
    Validate emitted event contains original candle.
    """

    candle = create_candle(
        datetime(
            2026,
            1,
            1,
            9,
            16,
        ),
        102.0,
    )

    engine = create_engine(
        (candle,),
    )

    event = next(engine.replay())

    assert event.candle is candle


def test_replay_engine_preserves_chronological_order() -> None:
    """
    Validate replay event ordering.
    """

    first = create_candle(
        datetime(
            2026,
            1,
            1,
            9,
            15,
        ),
        101.0,
    )

    second = create_candle(
        datetime(
            2026,
            1,
            1,
            9,
            16,
        ),
        102.0,
    )

    engine = create_engine(
        (
            first,
            second,
        ),
    )

    events = list(engine.replay())

    assert events[0].timestamp <= events[1].timestamp


def test_replay_engine_allows_empty_dataset() -> None:
    """
    Validate empty historical dataset behavior.
    """

    engine = create_engine(())

    events = list(engine.replay())

    assert events == []


def run_tests() -> None:
    """
    Execute all ReplayEngine validation tests.
    """

    tests = [
        test_replay_engine_initializes_with_valid_dependencies,
        test_replay_engine_exposes_provider_reference,
        test_replay_engine_exposes_clock_reference,
        test_replay_engine_rejects_invalid_provider,
        test_replay_engine_rejects_invalid_clock,
        test_replay_engine_preserves_dependency_identity,
        test_replay_engine_emits_replay_events,
        test_replay_engine_advances_clock_to_candle_time,
        test_replay_engine_preserves_candle_identity,
        test_replay_engine_preserves_chronological_order,
        test_replay_engine_allows_empty_dataset,
    ]

    for test in tests:
        test()
        print(f"PASSED: {test.__name__}")


if __name__ == "__main__":
    run_tests()