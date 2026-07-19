"""
Project Falcon SMA Test
"""

from datetime import datetime

from app.indicators.sma import SMA
from app.market.candle import Candle
from app.market.timeframe import TimeFrame


def build(close: float) -> Candle:
    return Candle(
        timestamp=datetime.now(),
        open=close,
        high=close,
        low=close,
        close=close,
        volume=100,
        timeframe=TimeFrame.FIVE_MINUTES,
    )


def main() -> None:
    print("=" * 50)
    print("Project Falcon SMA Test")
    print("=" * 50)

    closes = [
        10,
        11,
        12,
        13,
        14,
        15,
        16,
    ]

    candles = [build(value) for value in closes]

    sma = SMA(period=5)

    values = sma.calculate(candles)

    print(f"Indicator : {sma.name}")
    print(f"Values     : {len(values)}")
    print(f"First SMA  : {values[0]:.2f}")
    print(f"Last SMA   : {values[-1]:.2f}")

    assert len(values) == 3
    assert abs(values[0] - 12.0) < 0.0001
    assert abs(values[-1] - 14.0) < 0.0001

    print("\nSTATUS : PASS")


if __name__ == "__main__":
    main()