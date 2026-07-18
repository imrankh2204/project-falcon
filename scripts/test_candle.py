"""
Project Falcon Candle Validation
"""

from datetime import datetime

from app.market.candle import Candle
from app.market.timeframe import TimeFrame


def main() -> None:
    print("=" * 50)
    print("Project Falcon Candle Test")
    print("=" * 50)

    candle = Candle(
        timestamp=datetime(2026, 7, 18, 9, 15),
        open=25000.0,
        high=25040.5,
        low=24990.2,
        close=25032.8,
        volume=125000,
        timeframe=TimeFrame.FIVE_MINUTES,
    )

    print(f"Time       : {candle.timestamp}")
    print(f"Open       : {candle.open}")
    print(f"High       : {candle.high}")
    print(f"Low        : {candle.low}")
    print(f"Close      : {candle.close}")
    print(f"Volume     : {candle.volume}")
    print(f"TimeFrame  : {candle.timeframe}")

    print()

    print(f"Bullish    : {candle.is_bullish}")
    print(f"Bearish    : {candle.is_bearish}")
    print(f"Body Size  : {candle.body_size:.2f}")
    print(f"Range      : {candle.range:.2f}")

    assert candle.is_bullish
    assert not candle.is_bearish
    assert candle.range > 0

    print("\nSTATUS : PASS")


if __name__ == "__main__":
    main()