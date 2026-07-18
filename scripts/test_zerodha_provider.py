"""
Project Falcon ZerodhaMarketDataProvider Validation
"""

from app.broker.zerodha_broker import ZerodhaBroker
from app.services.providers.market_provider import MarketDataProvider
from app.services.providers.zerodha_provider import (
    ZerodhaMarketDataProvider,
)


def main() -> None:
    print("=" * 50)
    print("Project Falcon Zerodha Provider Test")
    print("=" * 50)

    broker = ZerodhaBroker()

    provider = ZerodhaMarketDataProvider(broker)

    print(f"Provider : {type(provider).__name__}")
    print(f"Broker   : {type(provider.broker).__name__}")

    assert isinstance(provider, MarketDataProvider)

    print("\nSTATUS : PASS")


if __name__ == "__main__":
    main()