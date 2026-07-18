"""
Project Falcon MarketDataProvider Validation
"""

from app.services.providers.market_provider import (
    MarketDataProvider,
)


def main() -> None:
    print("=" * 50)
    print("Project Falcon Market Provider Test")
    print("=" * 50)

    print()

    methods = [
        "get_historical_data",
        "get_latest_candle",
        "get_ltp",
    ]

    for method in methods:
        assert hasattr(MarketDataProvider, method)
        print(f"Found : {method}")

    print("\nSTATUS : PASS")


if __name__ == "__main__":
    main()