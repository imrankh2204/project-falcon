"""
Market data service for Project Falcon.

Provides a broker-independent interface for market data
consumption throughout the application.
"""

from __future__ import annotations

from app.market.candle import Candle
from app.market.instrument import Instrument
from app.market.timeframe import TimeFrame
from app.services.providers.market_provider import (
    MarketDataProvider,
)


class MarketDataService:
    """
    Application-facing market data service.
    """

    def __init__(self, provider: MarketDataProvider) -> None:
        self._provider = provider

    @property
    def provider(self) -> MarketDataProvider:
        """
        Return the configured market data provider.
        """
        return self._provider

    def get_historical_data(
        self,
        instrument: Instrument,
        timeframe: TimeFrame,
        count: int,
    ) -> list[Candle]:
        """
        Retrieve historical candles.
        """
        return self._provider.get_historical_data(
            instrument,
            timeframe,
            count,
        )

    def get_latest_candle(
        self,
        instrument: Instrument,
        timeframe: TimeFrame,
    ) -> Candle:
        """
        Retrieve the latest completed candle.
        """
        return self._provider.get_latest_candle(
            instrument,
            timeframe,
        )

    def get_ltp(
        self,
        instrument: Instrument,
    ) -> float:
        """
        Retrieve the latest traded price.
        """
        return self._provider.get_ltp(
            instrument,
        )