"""
Project Falcon MovingAverage Test
"""

from app.indicators.ema import EMA
from app.indicators.moving_average import MovingAverage


def main() -> None:
    print("=" * 50)
    print("Project Falcon Moving Average Test")
    print("=" * 50)

    ema = EMA(20)

    print(f"Indicator : {ema.name}")
    print(f"Period    : {ema.period}")

    assert isinstance(ema, MovingAverage)

    print("\nSTATUS : PASS")


if __name__ == "__main__":
    main()