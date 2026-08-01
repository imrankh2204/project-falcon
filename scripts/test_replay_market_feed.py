"""
Project Falcon

FAL-600-R2

ReplayMarketFeed validation.
"""

from __future__ import annotations

from datetime import datetime

from app.backtest.historical_provider import (
    HistoricalDataProvider,
)
from app.backtest.replay_clock import ReplayClock
from app.backtest.replay_engine import ReplayEngine
from app.live.replay_market_feed import ReplayMarketFeed
from app.market.candle import Candle
from app.market.timeframe import TimeFrame


class InMemoryHistoricalProvider(
    HistoricalDataProvider,
):
    """
    Simple in-memory provider for deterministic testing.
    """

    def __init__(
        self,
        candles,
    ):
        self._candles = tuple(candles)

    def candles(self):
        return iter(self._candles)


def main() -> None:

    candles = (
        Candle(
            timestamp=datetime.now(),
            timeframe=TimeFrame.ONE_MINUTE,
            open=100,
            high=101,
            low=99,
            close=100,
            volume=1000,
        ),
        Candle(
            timestamp=datetime.now(),
            timeframe=TimeFrame.ONE_MINUTE,
            open=101,
            high=102,
            low=100,
            close=101,
            volume=1000,
        ),
    )

    provider = InMemoryHistoricalProvider(
        candles,
    )

    start_time = candles[0].timestamp

    clock = ReplayClock(
        start_time=start_time,
    )

    replay_engine = ReplayEngine(
        provider=provider,
        clock=clock,
    )

    feed = ReplayMarketFeed(
        replay_engine,
    )

    feed.start()

    print("PASS: Feed started")

    events = tuple(feed.events())

    assert len(events) == 2

    print("PASS: Events replayed")

    feed.stop()

    print("PASS: Feed stopped")

    print()

    print("FAL-600-R2 COMPLETE")


if __name__ == "__main__":
    main()