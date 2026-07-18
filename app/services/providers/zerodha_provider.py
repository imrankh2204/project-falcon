"""
Zerodha market data provider for Project Falcon.

Consumes market data using an existing ZerodhaBroker instance.
"""

from __future__ import annotations

from app.broker.zerodha_broker import ZerodhaBroker
from app.market.candle import Candle
from app.market.instrument import Instrument
from app.market.timeframe import TimeFrame
from app.services.providers.market_provider import MarketDataProvider


class ZerodhaMarketDataProvider(MarketDataProvider):
    """
    Market data provider backed by Zerodha.
    """

    def __init__(self, broker: ZerodhaBroker) -> None:
        self._broker = broker

    @property
    def broker(self) -> ZerodhaBroker:
        """
        Return the underlying broker instance.
        """
        return self._broker

    def get_historical_data(
        self,
        instrument: Instrument,
        timeframe: TimeFrame,
        count: int,
    ) -> list[Candle]:
        raise NotImplementedError(
            "Historical data retrieval not implemented yet."
        )

    def get_latest_candle(
        self,
        instrument: Instrument,
        timeframe: TimeFrame,
    ) -> Candle:
        raise NotImplementedError(
            "Latest candle retrieval not implemented yet."
        )

    def get_ltp(
        self,
        instrument: Instrument,
    ) -> float:
        raise NotImplementedError(
            "LTP retrieval not implemented yet."
        )