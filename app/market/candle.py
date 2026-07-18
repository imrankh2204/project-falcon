"""
Candle domain model for Project Falcon.

Represents one completed OHLCV market candle.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from app.market.timeframe import TimeFrame


@dataclass(frozen=True, slots=True)
class Candle:
    """
    Immutable OHLCV candle.

    Attributes
    ----------
    timestamp:
        Start time of the candle.
    open:
        Opening price.
    high:
        Highest traded price.
    low:
        Lowest traded price.
    close:
        Closing price.
    volume:
        Traded volume.
    timeframe:
        Candle timeframe.
    """

    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int
    timeframe: TimeFrame

    @property
    def is_bullish(self) -> bool:
        """
        True when the candle closes above its open.
        """

        return self.close > self.open

    @property
    def is_bearish(self) -> bool:
        """
        True when the candle closes below its open.
        """

        return self.close < self.open

    @property
    def body_size(self) -> float:
        """
        Absolute candle body size.
        """

        return abs(self.close - self.open)

    @property
    def range(self) -> float:
        """
        Total candle range.
        """

        return self.high - self.low