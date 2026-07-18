"""
Project Falcon MarketDataNormalizer Batch Test
"""

from app.market.timeframe import TimeFrame
from app.services.normalizer import MarketDataNormalizer


def main() -> None:
    print("=" * 50)
    print("Project Falcon Batch Normalizer Test")
    print("=" * 50)

    payloads = [
        {
            "date": "2026-07-18T09:15:00",
            "open": 25000,
            "high": 25040,
            "low": 24990,
            "close": 25030,
            "volume": 120000,
        },
        {
            "date": "2026-07-18T09:20:00",
            "open": 25030,
            "high": 25060,
            "low": 25020,
            "close": 25055,
            "volume": 118500,
        },
        {
            "date": "2026-07-18T09:25:00",
            "open": 25055,
            "high": 25080,
            "low": 25050,
            "close": 25075,
            "volume": 132000,
        },
    ]

    candles = MarketDataNormalizer.candles_from_ohlc(
        payloads,
        TimeFrame.FIVE_MINUTES,
    )

    print(f"Total Candles : {len(candles)}")
    print(f"First Close   : {candles[0].close}")
    print(f"Last Close    : {candles[-1].close}")
    print(f"TimeFrame     : {candles[-1].timeframe}")

    assert len(candles) == 3
    assert candles[0].close == 25030.0
    assert candles[-1].close == 25075.0
    assert candles[-1].timeframe is TimeFrame.FIVE_MINUTES

    print("\nSTATUS : PASS")


if __name__ == "__main__":
    main()