"""
Moving Average base class for Project Falcon.
"""

from __future__ import annotations

from abc import abstractmethod

from app.indicators.indicator import Indicator
from app.market.candle import Candle


class MovingAverage(Indicator):
    """
    Shared functionality for moving averages.
    """

    def __init__(self, period: int) -> None:
        if period <= 0:
            raise ValueError(
                "period must be greater than zero."
            )

        self._period = period

    @property
    def period(self) -> int:
        """
        Moving average lookback period.
        """
        return self._period

    def validate(
        self,
        candles: list[Candle],
    ) -> None:
        """
        Validate candle input.
        """

        if len(candles) < self.period:
            raise ValueError(
                "Not enough candles to calculate indicator."
            )

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Indicator name.
        """

    @abstractmethod
    def calculate(
        self,
        candles: list[Candle],
    ):
        """
        Calculate moving average.
        """