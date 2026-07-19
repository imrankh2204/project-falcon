"""
Exponential Moving Average indicator for Project Falcon.
"""

from __future__ import annotations

from app.indicators.moving_average import MovingAverage
from app.market.candle import Candle


class EMA(MovingAverage):
    """
    Exponential Moving Average.
    """

    @property
    def name(self) -> str:
        return f"EMA({self.period})"

    def calculate(
        self,
        candles: list[Candle],
    ) -> list[float]:

        self.validate(candles)

        closes = [candle.close for candle in candles]

        multiplier = 2 / (self.period + 1)

        sma = sum(closes[: self.period]) / self.period

        ema_values = [sma]

        previous = sma

        for close in closes[self.period:]:
            current = (
                (close - previous) * multiplier
            ) + previous

            ema_values.append(current)

            previous = current

        return ema_values