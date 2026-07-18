"""
Project Falcon MarketDataService Validation
"""

from app.broker.zerodha_broker import ZerodhaBroker
from app.services.market_data import MarketDataService
from app.services.providers.market_provider import (
    MarketDataProvider,
)
from app.services.providers.zerodha_provider import (
    ZerodhaMarketDataProvider,
)


def main() -> None:
    print("=" * 50)
    print("Project Falcon Market Data Service Test")
    print("=" * 50)

    broker = ZerodhaBroker()

    provider = ZerodhaMarketDataProvider(broker)

    service = MarketDataService(provider)

    print(f"Service  : {type(service).__name__}")
    print(f"Provider : {type(service.provider).__name__}")

    assert isinstance(service.provider, MarketDataProvider)

    print("\nSTATUS : PASS")


if __name__ == "__main__":
    main()