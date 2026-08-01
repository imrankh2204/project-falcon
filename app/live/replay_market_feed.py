"""
Project Falcon

FAL-600-R2

Replay Market Feed

Adapts ReplayEngine to the MarketFeed contract.

Responsibilities
----------------
- Expose ReplayEngine as a MarketFeed.
- Preserve deterministic replay ordering.
- Remain broker independent.

The adapter intentionally does NOT implement:

- Replay logic
- Strategy execution
- Event transformation
- Runtime coordination
"""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any

from app.backtest.replay_engine import ReplayEngine
from app.live.market_feed import MarketFeed


class ReplayMarketFeed(MarketFeed):
    """
    Adapter exposing ReplayEngine through the MarketFeed interface.
    """

    def __init__(
        self,
        replay_engine: ReplayEngine,
    ) -> None:

        if not isinstance(
            replay_engine,
            ReplayEngine,
        ):
            raise TypeError(
                "replay_engine must be a ReplayEngine."
            )

        self._replay_engine = replay_engine

        self._started = False

    def start(self) -> None:
        """
        Start the replay feed.
        """

        self._started = True

    def stop(self) -> None:
        """
        Stop the replay feed.
        """

        self._started = False

    def events(self) -> Iterable[Any]:
        """
        Yield replay events from ReplayEngine.
        """

        if not self._started:
            raise RuntimeError(
                "ReplayMarketFeed has not been started."
            )

        yield from self._replay_engine.replay()