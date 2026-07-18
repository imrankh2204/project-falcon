"""
Market data normalization utilities for Project Falcon.
"""

from __future__ import annotations

from datetime import datetime

from app.market.candle import Candle
from app.market.timeframe import TimeFrame


class MarketDataNormalizer:
    """
    Converts broker payloads into Falcon domain objects.
    """

    @staticmethod
    def candle_from_ohlc(
        payload: dict,
        timeframe: TimeFrame,
    ) -> Candle:
        """
        Convert a broker OHLC payload into a Candle.
        """

        required = (
            "date",
            "open",
            "high",
            "low",
            "close",
            "volume",
        )

        missing = [key for key in required if key not in payload]

        if missing:
            raise ValueError(
                f"Missing required candle fields: {', '.join(missing)}"
            )

        timestamp = payload["date"]

        if isinstance(timestamp, str):
            timestamp = datetime.fromisoformat(timestamp)

        if not isinstance(timestamp, datetime):
            raise TypeError(
                "date must be a datetime or ISO-8601 string."
            )

        return Candle(
            timestamp=timestamp,
            open=float(payload["open"]),
            high=float(payload["high"]),
            low=float(payload["low"]),
            close=float(payload["close"]),
            volume=int(payload["volume"]),
            timeframe=timeframe,
        )

    @staticmethod
    def candles_from_ohlc(
        payloads: list[dict],
        timeframe: TimeFrame,
    ) -> list[Candle]:
        """
        Convert multiple broker payloads into Falcon Candle objects.
        """

        return [
            MarketDataNormalizer.candle_from_ohlc(
                payload,
                timeframe,
            )
            for payload in payloads
        ]