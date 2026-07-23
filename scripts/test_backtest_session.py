"""
Smoke tests for BacktestSession.

Validates application orchestration during historical replay.
"""

from __future__ import annotations

from collections.abc import Iterable
from datetime import datetime

from app.backtest.backtest_session import BacktestSession
from app.backtest.historical_provider import HistoricalDataProvider
from app.backtest.replay_clock import ReplayClock
from app.backtest.replay_engine import ReplayEngine
from app.market.candle import Candle
from app.market.instrument import Instrument
from app.market.timeframe import TimeFrame
from app.strategies.context import StrategyContext
from app.strategies.signal import Signal
from app.strategies.strategy import Strategy


class DummyHistoricalProvider(HistoricalDataProvider):
    """
    Simple historical provider used for testing.
    """

    def __init__(
        self,
        candles: Iterable[Candle],
    ) -> None:
        self._candles = list(candles)

    def candles(self) -> Iterable[Candle]:
        return iter(self._candles)


class RecordingStrategy(Strategy):
    """
    Records every received StrategyContext.
    """

    def __init__(self) -> None:
        self.contexts: list[StrategyContext] = []

    @property
    def name(self) -> str:
        return "RecordingStrategy"

    def evaluate(
        self,
        context: StrategyContext,
    ) -> Signal:
        self.contexts.append(context)
        return Signal.HOLD


class FailingStrategy(Strategy):
    """
    Strategy used to verify exception propagation.
    """

    @property
    def name(self) -> str:
        return "FailingStrategy"

    def evaluate(
        self,
        context: StrategyContext,
    ) -> Signal:
        raise RuntimeError(
            "Strategy failure."
        )


def create_instrument() -> Instrument:
    """
    Create a reusable test instrument.
    """

    return Instrument(
        exchange="NSE",
        symbol="NIFTY",
        instrument_token=12345,
        lot_size=50,
        tick_size=0.05,
    )


def create_candle(
    minute: int,
) -> Candle:
    """
    Create a deterministic candle.
    """

    return Candle(
        timestamp=datetime(
            2025,
            1,
            1,
            9,
            minute,
        ),
        open=100.0 + minute,
        high=101.0 + minute,
        low=99.0 + minute,
        close=100.5 + minute,
        volume=1000,
        timeframe=TimeFrame.ONE_MINUTE,
    )


def create_session(
    candles: Iterable[Candle],
    strategy: Strategy,
) -> BacktestSession:
    """
    Build a BacktestSession for testing.
    """

    provider = DummyHistoricalProvider(candles)

    clock = ReplayClock(
        start_time=datetime(
            2025,
            1,
            1,
            9,
            0,
        )
    )

    engine = ReplayEngine(
        provider=provider,
        clock=clock,
    )

    return BacktestSession(
        replay_engine=engine,
        instrument=create_instrument(),
        strategy=strategy,
    )

def test_backtest_session_initializes_with_valid_dependencies() -> None:
    """
    Verify construction succeeds with valid dependencies.
    """

    strategy = RecordingStrategy()

    session = create_session(
        candles=[],
        strategy=strategy,
    )

    assert isinstance(session, BacktestSession)


def test_backtest_session_exposes_replay_engine_reference() -> None:
    """
    Verify the replay engine reference is preserved.
    """

    strategy = RecordingStrategy()

    session = create_session(
        candles=[],
        strategy=strategy,
    )

    assert isinstance(
        session.replay_engine,
        ReplayEngine,
    )


def test_backtest_session_exposes_instrument_reference() -> None:
    """
    Verify the instrument reference is preserved.
    """

    strategy = RecordingStrategy()

    session = create_session(
        candles=[],
        strategy=strategy,
    )

    instrument = create_instrument()

    assert session.instrument == instrument


def test_backtest_session_exposes_strategy_reference() -> None:
    """
    Verify the strategy reference is preserved.
    """

    strategy = RecordingStrategy()

    session = create_session(
        candles=[],
        strategy=strategy,
    )

    assert session.strategy is strategy


def test_backtest_session_rejects_invalid_replay_engine() -> None:
    """
    ReplayEngine dependency must be validated.
    """

    try:
        BacktestSession(
            replay_engine=object(),
            instrument=create_instrument(),
            strategy=RecordingStrategy(),
        )

    except TypeError:
        return

    raise AssertionError(
        "Expected TypeError."
    )


def test_backtest_session_rejects_invalid_instrument() -> None:
    """
    Instrument dependency must be validated.
    """

    provider = DummyHistoricalProvider([])

    clock = ReplayClock(
        start_time=datetime(
            2025,
            1,
            1,
            9,
            0,
        )
    )

    engine = ReplayEngine(
        provider=provider,
        clock=clock,
    )

    try:
        BacktestSession(
            replay_engine=engine,
            instrument=object(),
            strategy=RecordingStrategy(),
        )

    except TypeError:
        return

    raise AssertionError(
        "Expected TypeError."
    )


def test_backtest_session_rejects_invalid_strategy() -> None:
    """
    Strategy dependency must be validated.
    """

    provider = DummyHistoricalProvider([])

    clock = ReplayClock(
        start_time=datetime(
            2025,
            1,
            1,
            9,
            0,
        )
    )

    engine = ReplayEngine(
        provider=provider,
        clock=clock,
    )

    try:
        BacktestSession(
            replay_engine=engine,
            instrument=create_instrument(),
            strategy=object(),
        )

    except TypeError:
        return

    raise AssertionError(
        "Expected TypeError."
    )

def test_backtest_session_runs_complete_replay() -> None:
    """
    Verify every replay event is evaluated.
    """

    strategy = RecordingStrategy()

    session = create_session(
        candles=[
            create_candle(0),
            create_candle(1),
            create_candle(2),
        ],
        strategy=strategy,
    )

    session.run()

    assert len(strategy.contexts) == 3


def test_backtest_session_passes_correct_instrument() -> None:
    """
    Every StrategyContext should contain the configured instrument.
    """

    strategy = RecordingStrategy()

    session = create_session(
        candles=[
            create_candle(0),
            create_candle(1),
        ],
        strategy=strategy,
    )

    expected = session.instrument

    session.run()

    for context in strategy.contexts:
        assert context.instrument == expected


def test_backtest_session_passes_correct_timeframe() -> None:
    """
    StrategyContext should use the current candle timeframe.
    """

    strategy = RecordingStrategy()

    session = create_session(
        candles=[
            create_candle(0),
            create_candle(1),
        ],
        strategy=strategy,
    )

    session.run()

    assert strategy.contexts[0].timeframe == TimeFrame.ONE_MINUTE
    assert strategy.contexts[1].timeframe == TimeFrame.ONE_MINUTE


def test_backtest_session_builds_cumulative_history() -> None:
    """
    Candle history should grow one candle at a time.
    """

    strategy = RecordingStrategy()

    session = create_session(
        candles=[
            create_candle(0),
            create_candle(1),
            create_candle(2),
        ],
        strategy=strategy,
    )

    session.run()

    assert len(strategy.contexts[0].candles) == 1
    assert len(strategy.contexts[1].candles) == 2
    assert len(strategy.contexts[2].candles) == 3


def test_backtest_session_preserves_candle_order() -> None:
    """
    Candle ordering must remain chronological.
    """

    strategy = RecordingStrategy()

    candles = [
        create_candle(0),
        create_candle(1),
        create_candle(2),
    ]

    session = create_session(
        candles=candles,
        strategy=strategy,
    )

    session.run()

    final_history = strategy.contexts[-1].candles

    assert final_history == candles


def test_backtest_session_passes_independent_history_lists() -> None:
    """
    Every StrategyContext should own its own candle list.
    """

    strategy = RecordingStrategy()

    session = create_session(
        candles=[
            create_candle(0),
            create_candle(1),
            create_candle(2),
        ],
        strategy=strategy,
    )

    session.run()

    assert (
        strategy.contexts[0].candles
        is not strategy.contexts[1].candles
    )

    assert (
        strategy.contexts[1].candles
        is not strategy.contexts[2].candles
    )

class FailingHistoricalProvider(HistoricalDataProvider):
    """
    Historical provider used to verify replay exception propagation.
    """

    def candles(self) -> Iterable[Candle]:
        raise RuntimeError(
            "Replay failure."
        )


def test_backtest_session_allows_empty_replay() -> None:
    """
    Empty replay datasets should complete successfully.
    """

    strategy = RecordingStrategy()

    session = create_session(
        candles=[],
        strategy=strategy,
    )

    session.run()

    assert strategy.contexts == []


def test_backtest_session_propagates_strategy_exceptions() -> None:
    """
    Strategy exceptions must propagate unchanged.
    """

    session = create_session(
        candles=[
            create_candle(0),
        ],
        strategy=FailingStrategy(),
    )

    try:
        session.run()

    except RuntimeError as ex:
        assert str(ex) == "Strategy failure."
        return

    raise AssertionError(
        "Expected RuntimeError."
    )


def test_backtest_session_propagates_replay_exceptions() -> None:
    """
    Replay exceptions must propagate unchanged.
    """

    clock = ReplayClock(
        start_time=datetime(
            2025,
            1,
            1,
            9,
            0,
        )
    )

    engine = ReplayEngine(
        provider=FailingHistoricalProvider(),
        clock=clock,
    )

    session = BacktestSession(
        replay_engine=engine,
        instrument=create_instrument(),
        strategy=RecordingStrategy(),
    )

    try:
        session.run()

    except RuntimeError as ex:
        assert str(ex) == "Replay failure."
        return

    raise AssertionError(
        "Expected RuntimeError."
    )


def run_test(
    test,
) -> None:
    """
    Execute one smoke test.
    """

    test()

    print(
        f"PASSED: {test.__name__}"
    )


if __name__ == "__main__":
    TESTS = (
        test_backtest_session_initializes_with_valid_dependencies,
        test_backtest_session_exposes_replay_engine_reference,
        test_backtest_session_exposes_instrument_reference,
        test_backtest_session_exposes_strategy_reference,
        test_backtest_session_rejects_invalid_replay_engine,
        test_backtest_session_rejects_invalid_instrument,
        test_backtest_session_rejects_invalid_strategy,
        test_backtest_session_runs_complete_replay,
        test_backtest_session_passes_correct_instrument,
        test_backtest_session_passes_correct_timeframe,
        test_backtest_session_builds_cumulative_history,
        test_backtest_session_preserves_candle_order,
        test_backtest_session_passes_independent_history_lists,
        test_backtest_session_allows_empty_replay,
        test_backtest_session_propagates_strategy_exceptions,
        test_backtest_session_propagates_replay_exceptions,
    )

    for test in TESTS:
        run_test(test)