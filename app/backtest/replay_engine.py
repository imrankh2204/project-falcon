"""
Replay engine for Project Falcon.

Coordinates deterministic historical replay execution.

Responsibilities:
    - Own replay dependencies.
    - Validate replay components.
    - Consume historical candles.
    - Synchronize ReplayClock progression.
    - Emit immutable ReplayEvent objects.

The ReplayEngine intentionally does NOT implement:

    - Strategy execution
    - Signal generation
    - Order execution
    - Portfolio updates
    - Performance reporting
"""

from __future__ import annotations

from collections.abc import Iterator

from app.backtest.historical_provider import HistoricalDataProvider
from app.backtest.replay_clock import ReplayClock
from app.backtest.replay_event import ReplayEvent


class ReplayEngine:
    """
    Coordinates deterministic historical replay.

    The ReplayEngine connects historical market data with the
    replay timeline. Each consumed candle advances the replay
    clock and produces a ReplayEvent for downstream consumers.

    Parameters
    ----------
    provider:
        Historical data source.

    clock:
        Deterministic replay clock.

    Raises
    ------
    TypeError
        If dependencies do not match the required contracts.
    """

    def __init__(
        self,
        provider: HistoricalDataProvider,
        clock: ReplayClock,
    ) -> None:
        """
        Initialize the replay engine.

        Parameters
        ----------
        provider:
            Historical data provider.

        clock:
            Deterministic replay clock.

        Raises
        ------
        TypeError
            If either dependency has an invalid type.
        """

        if not isinstance(provider, HistoricalDataProvider):
            raise TypeError(
                "provider must be a HistoricalDataProvider."
            )

        if not isinstance(clock, ReplayClock):
            raise TypeError(
                "clock must be a ReplayClock."
            )

        self._provider = provider
        self._clock = clock

    @property
    def provider(self) -> HistoricalDataProvider:
        """
        Return the configured historical data provider.

        Returns
        -------
        HistoricalDataProvider
            Provider used for replay input.
        """

        return self._provider

    @property
    def clock(self) -> ReplayClock:
        """
        Return the configured replay clock.

        Returns
        -------
        ReplayClock
            Clock controlling simulated replay time.
        """

        return self._clock

    def replay(self) -> Iterator[ReplayEvent]:
        """
        Replay historical candles deterministically.

        Each candle from the historical provider advances the
        replay clock and is converted into a ReplayEvent.

        Yields
        ------
        ReplayEvent
            Immutable replay event containing timestamp and candle.

        Notes
        -----
        Empty historical datasets are supported and result in
        an empty iterator.
        """

        for candle in self._provider.candles():
            self._clock.advance(candle.timestamp)

            yield ReplayEvent(
                timestamp=candle.timestamp,
                candle=candle,
            )