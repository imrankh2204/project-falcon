"""
Backtest session for Project Falcon.

Coordinates deterministic historical replay with strategy evaluation.

Responsibilities:
    - Own the replay session lifecycle.
    - Validate application dependencies.
    - Execute deterministic replay.
    - Build StrategyContext instances.
    - Invoke trading strategies.

The BacktestSession intentionally does NOT implement:

    - Order execution
    - Portfolio management
    - Risk management
    - Performance reporting
    - Signal interpretation
"""

from __future__ import annotations

from app.backtest.replay_engine import ReplayEngine
from app.market.candle import Candle
from app.market.instrument import Instrument
from app.strategies.context import StrategyContext
from app.strategies.strategy import Strategy


class BacktestSession:
    """
    Application service coordinating historical replay.

    A BacktestSession composes the replay infrastructure with the
    strategy domain. During replay it maintains cumulative market
    history, constructs StrategyContext objects, and invokes the
    configured strategy for every replay event.

    The strategy output is intentionally ignored during this
    milestone. Future milestones will translate strategy signals
    into executable trading decisions.
    """

    def __init__(
        self,
        replay_engine: ReplayEngine,
        instrument: Instrument,
        strategy: Strategy,
    ) -> None:
        """
        Initialize the backtest session.

        Parameters
        ----------
        replay_engine:
            Replay engine used to execute historical replay.

        instrument:
            Instrument associated with the replay session.

        strategy:
            Strategy evaluated during replay.

        Raises
        ------
        TypeError
            If any dependency has an invalid type.
        """

        if not isinstance(replay_engine, ReplayEngine):
            raise TypeError(
                "replay_engine must be a ReplayEngine."
            )

        if not isinstance(instrument, Instrument):
            raise TypeError(
                "instrument must be an Instrument."
            )

        if not isinstance(strategy, Strategy):
            raise TypeError(
                "strategy must be a Strategy."
            )

        self._replay_engine = replay_engine
        self._instrument = instrument
        self._strategy = strategy

    @property
    def replay_engine(self) -> ReplayEngine:
        """
        Return the replay engine owned by this session.
        """

        return self._replay_engine

    @property
    def instrument(self) -> Instrument:
        """
        Return the instrument associated with this session.
        """

        return self._instrument

    @property
    def strategy(self) -> Strategy:
        """
        Return the strategy evaluated during replay.
        """

        return self._strategy

    def run(self) -> None:
        """
        Execute the backtest session.

        The replay engine is consumed sequentially. For each replay
        event, the cumulative candle history is updated, a new
        StrategyContext is constructed, and the configured strategy
        is evaluated.

        The returned Signal is intentionally ignored during this
        milestone.

        Empty replay datasets are treated as successful execution.

        Raises
        ------
        Exception
            Any exception raised by the replay engine or strategy is
            propagated unchanged.
        """

        history: list[Candle] = []

        for replay_event in self._replay_engine.replay():
            history.append(replay_event.candle)

            context = self._build_context(history)

            self._strategy.evaluate(context)

    def _build_context(
        self,
        candles: list[Candle],
    ) -> StrategyContext:
        """
        Build a strategy context for the current replay state.

        Parameters
        ----------
        candles:
            Cumulative candle history observed during replay.

        Returns
        -------
        StrategyContext
            Immutable snapshot supplied to the strategy.
        """

        if not candles:
            raise ValueError(
                "StrategyContext requires at least one candle."
            )

        return StrategyContext(
            instrument=self._instrument,
            timeframe=candles[-1].timeframe,
            candles=list(candles),
        )