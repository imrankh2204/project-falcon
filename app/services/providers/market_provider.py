"""
Market data provider abstraction for Project Falcon.

Defines the interface implemented by all market
data providers.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.market.candle import Candle
from app.market.instrument import Instrument
from app.market.timeframe import TimeFrame


class MarketDataProvider(ABC):
    """
    Abstract market data provider.
    """

    @abstractmethod
    def get_historical_data(
        self,
        instrument: Instrument,
        timeframe: TimeFrame,
        count: int,
    ) -> list[Candle]:
        """
        Return historical candles.
        """

    @abstractmethod
    def get_latest_candle(
        self,
        instrument: Instrument,
        timeframe: TimeFrame,
    ) -> Candle:
        """
        Return the latest completed candle.
        """

    @abstractmethod
    def get_ltp(
        self,
        instrument: Instrument,
    ) -> float:
        """
        Return latest traded price.
        """