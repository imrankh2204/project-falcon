"""
Simple Moving Average indicator for Project Falcon.
"""

from __future__ import annotations

from app.indicators.moving_average import MovingAverage
from app.market.candle import Candle


class SMA(MovingAverage):
    """
    Simple Moving Average.
    """

    @property
    def name(self) -> str:
        return f"SMA({self.period})"

    def calculate(
        self,
        candles: list[Candle],
    ) -> list[float]:
        """
        Calculate Simple Moving Average values.
        """

        self.validate(candles)

        closes = [candle.close for candle in candles]

        values: list[float] = []

        for index in range(
            self.period - 1,
            len(closes),
        ):
            window = closes[
                index - self.period + 1 : index + 1
            ]

            values.append(
                sum(window) / self.period
            )

        return values