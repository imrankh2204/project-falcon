"""
Smoke tests for BacktestSession.

These tests validate the orchestration responsibilities of the
BacktestSession application service.

The suite intentionally uses only the Python standard library and
simple fake implementations to remain lightweight and deterministic.
"""

from __future__ import annotations

from collections.abc import Iterator
from datetime import datetime

from app.backtest.backtest_session import BacktestSession
from app.backtest.historical_provider import HistoricalDataProvider
from app.backtest.replay_clock import ReplayClock
from app.backtest.replay_engine import ReplayEngine
from app.market.candle import Candle
from app.market.timeframe import TimeFrame


class FakeHistoricalProvider(HistoricalDataProvider):
    """
    Simple historical provider returning a predefined candle sequence.
    """

    def __init__(
        self,
        candles: list[Candle],
    ) -> None:
        self._candles = tuple(candles)

    def candles(self) -> Iterator[Candle]:
        return iter(self._candles)


class FailingHistoricalProvider(HistoricalDataProvider):
    """
    Historical provider that raises during iteration.
    """

    def candles(self) -> Iterator[Candle]:
        raise RuntimeError("Replay failure")


def _create_candle(
    minute: int,
) -> Candle:
    """
    Create a deterministic candle for testing.
    """

    timestamp = datetime(
        2025,
        1,
        1,
        9,
        minute,
        0,
    )

    return Candle(
        timestamp=timestamp,
        open=100.0,
        high=105.0,
        low=95.0,
        close=102.0,
        volume=1000,
        timeframe=TimeFrame.ONE_MINUTE,
    )


def _assert_raises(
    expected_exception: type[BaseException],
    func,
    *args,
    **kwargs,
) -> None:
    """
    Verify that the expected exception is raised.
    """

    try:
        func(*args, **kwargs)
    except expected_exception:
        return
    except Exception as exc:  # pragma: no cover
        raise AssertionError(
            f"Expected {expected_exception.__name__}, "
            f"got {type(exc).__name__}."
        ) from exc

    raise AssertionError(
        f"Expected {expected_exception.__name__}."
    )

def test_backtest_session_initializes_with_valid_replay_engine() -> None:
    """
    Verify a BacktestSession accepts a valid ReplayEngine.
    """

    provider = FakeHistoricalProvider([])
    clock = ReplayClock(datetime(2025, 1, 1, 9, 0, 0))
    replay_engine = ReplayEngine(provider, clock)

    session = BacktestSession(replay_engine)

    assert session.replay_engine is replay_engine


def test_backtest_session_exposes_replay_engine_reference() -> None:
    """
    Verify the replay engine reference is preserved.
    """

    provider = FakeHistoricalProvider([])
    clock = ReplayClock(datetime(2025, 1, 1, 9, 0, 0))
    replay_engine = ReplayEngine(provider, clock)

    session = BacktestSession(replay_engine)

    assert session.replay_engine is replay_engine


def test_backtest_session_rejects_invalid_replay_engine() -> None:
    """
    Verify constructor rejects invalid replay engine types.
    """

    _assert_raises(
        TypeError,
        BacktestSession,
        object(),
    )


def test_backtest_session_runs_complete_replay() -> None:
    """
    Verify the session consumes the replay to completion.
    """

    candles = [
        _create_candle(0),
        _create_candle(1),
        _create_candle(2),
    ]

    provider = FakeHistoricalProvider(candles)
    clock = ReplayClock(candles[0].timestamp)
    replay_engine = ReplayEngine(provider, clock)

    session = BacktestSession(replay_engine)

    session.run()

    assert replay_engine.clock.current_time == candles[-1].timestamp


def test_backtest_session_allows_empty_replay() -> None:
    """
    Verify an empty replay completes successfully.
    """

    provider = FakeHistoricalProvider([])
    clock = ReplayClock(datetime(2025, 1, 1, 9, 0, 0))
    replay_engine = ReplayEngine(provider, clock)

    session = BacktestSession(replay_engine)

    session.run()

    assert session.replay_engine is replay_engine


def test_backtest_session_propagates_replay_exceptions() -> None:
    """
    Verify replay exceptions propagate unchanged.
    """

    provider = FailingHistoricalProvider()
    clock = ReplayClock(datetime(2025, 1, 1, 9, 0, 0))
    replay_engine = ReplayEngine(provider, clock)

    session = BacktestSession(replay_engine)

    _assert_raises(
        RuntimeError,
        session.run,
    )


_TESTS = (
    test_backtest_session_initializes_with_valid_replay_engine,
    test_backtest_session_exposes_replay_engine_reference,
    test_backtest_session_rejects_invalid_replay_engine,
    test_backtest_session_runs_complete_replay,
    test_backtest_session_allows_empty_replay,
    test_backtest_session_propagates_replay_exceptions,
)


if __name__ == "__main__":
    for test in _TESTS:
        test()
        print(f"PASSED: {test.__name__}")