"""
Project Falcon EMA Calculation Test
"""

from datetime import datetime

from app.indicators.ema import EMA
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
    print("Project Falcon EMA Calculation Test")
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

    ema = EMA(period=5)

    values = ema.calculate(candles)

    print(f"Indicator : {ema.name}")
    print(f"Values     : {len(values)}")
    print(f"First EMA  : {values[0]:.2f}")
    print(f"Last EMA   : {values[-1]:.2f}")

    assert len(values) == 3
    assert abs(values[0] - 12.0) < 0.0001

    print("\nSTATUS : PASS")


if __name__ == "__main__":
    main()