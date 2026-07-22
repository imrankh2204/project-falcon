"""
Replay engine for Project Falcon.

Coordinates the replay infrastructure used during historical
backtesting.

Responsibilities:
    - Own the replay dependencies.
    - Validate replay components.
    - Expose replay infrastructure.

The ReplayEngine intentionally does NOT implement:

    - Historical replay loop
    - Strategy execution
    - Order execution
    - Portfolio updates
    - Performance reporting
"""

from __future__ import annotations

from app.backtest.historical_provider import HistoricalDataProvider
from app.backtest.replay_clock import ReplayClock


class ReplayEngine:
    """
    Coordinates the replay infrastructure.

    The ReplayEngine owns the historical data provider and the
    replay clock. Future revisions will use these dependencies to
    replay historical candles through the existing trading domain.
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
        Return the historical data provider.
        """
        return self._provider

    @property
    def clock(self) -> ReplayClock:
        """
        Return the replay clock.
        """
        return self._clock