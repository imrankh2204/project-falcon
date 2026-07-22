"""
Smoke tests for the Backtest infrastructure.

Run:

    python scripts/test_backtest.py
"""

from __future__ import annotations

from datetime import datetime

from app.backtest import (
    HistoricalDataProvider,
    ReplayClock,
    ReplayEngine,
)


class DummyProvider(HistoricalDataProvider):
    """
    Minimal historical provider used for smoke testing.
    """

    def candles(self):
        """
        Return an empty candle sequence.
        """
        return []


def main() -> None:
    """
    Execute backtest smoke tests.
    """

    print("=" * 60)
    print("Backtest Smoke Test")
    print("=" * 60)

    #
    # Package imports
    #

    print("\n[1] Verify package imports...")

    assert HistoricalDataProvider is not None
    assert ReplayClock is not None
    assert ReplayEngine is not None

    print("✓ Package imports verified")

    #
    # Historical provider
    #

    print("\n[2] Verify HistoricalDataProvider...")

    provider = DummyProvider()

    assert list(provider.candles()) == []

    print("✓ HistoricalDataProvider verified")

    #
    # Replay clock
    #

    print("\n[3] Verify ReplayClock...")

    start_time = datetime(
        2026,
        1,
        1,
        9,
        15,
    )

    clock = ReplayClock(start_time)

    assert clock.current_time == start_time

    next_time = datetime(
        2026,
        1,
        1,
        9,
        16,
    )

    clock.advance(next_time)

    assert clock.current_time == next_time

    try:
        clock.advance(start_time)
        raise AssertionError(
            "Expected ValueError was not raised."
        )

    except ValueError:
        pass

    print("✓ ReplayClock verified")

    #
    # Replay engine
    #

    print("\n[4] Verify ReplayEngine...")

    engine = ReplayEngine(
        provider=provider,
        clock=clock,
    )

    assert engine.provider is provider
    assert engine.clock is clock

    print("✓ ReplayEngine verified")

    print("\n" + "=" * 60)
    print("All Backtest smoke tests passed.")
    print("=" * 60)


if __name__ == "__main__":
    main()