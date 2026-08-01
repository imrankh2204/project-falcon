"""
Project Falcon

FAL-600-R3

Replay Runtime Validation

Validates that LiveRuntime consumes events through the
MarketFeed abstraction using ReplayMarketFeed.

This test intentionally verifies runtime orchestration only.
"""

from __future__ import annotations

from datetime import datetime

from app.backtest.historical_provider import HistoricalDataProvider
from app.backtest.replay_clock import ReplayClock
from app.backtest.replay_engine import ReplayEngine
from app.live.live_runtime import LiveRuntime
from app.live.replay_market_feed import ReplayMarketFeed
from app.market.candle import Candle
from app.market.timeframe import TimeFrame


class InMemoryHistoricalProvider(HistoricalDataProvider):
    """
    Simple deterministic provider used for testing.
    """

    def __init__(self, candles):
        self._candles = tuple(candles)

    def candles(self):
        return iter(self._candles)


class MockLiveEngine:
    """
    Records every processed replay event.
    """

    def __init__(self):
        self.events = []

    def start(self):
        pass

    def stop(self):
        pass

    def process_event(self, event):
        self.events.append(event)
        print(f"PASS: Event {len(self.events)} processed")


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
        Candle(
            timestamp=datetime.now(),
            timeframe=TimeFrame.ONE_MINUTE,
            open=102,
            high=103,
            low=101,
            close=102,
            volume=1000,
        ),
    )

    provider = InMemoryHistoricalProvider(candles)

    clock = ReplayClock(
        start_time=candles[0].timestamp,
    )

    replay_engine = ReplayEngine(
        provider=provider,
        clock=clock,
    )

    market_feed = ReplayMarketFeed(
        replay_engine,
    )

    engine = MockLiveEngine()

    runtime = LiveRuntime(
        live_engine=engine,
        market_feed=market_feed,
    )

    print("PASS: Runtime created")

    runtime.run()

    assert len(engine.events) == 3

    print("PASS: Runtime finished")
    print()
    print("FAL-600-R3 COMPLETE")


if __name__ == "__main__":
    main()