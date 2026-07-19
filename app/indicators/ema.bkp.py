"""
Exponential Moving Average indicator for Project Falcon.
"""

from __future__ import annotations

from app.indicators.indicator import Indicator
from app.market.candle import Candle


class EMA(Indicator):
    """
    Exponential Moving Average (EMA).
    """

    def __init__(self, period: int) -> None:
        if period <= 0:
            raise ValueError("period must be greater than zero.")

        self._period = period

    @property
    def period(self) -> int:
        """
        EMA lookback period.
        """
        return self._period

    @property
    def name(self) -> str:
        """
        Indicator name.
        """
        return f"EMA({self.period})"

    def calculate(
        self,
        candles: list[Candle],
    ) -> list[float]:
        """
        Calculate the Exponential Moving Average.

        Returns a list beginning with the first valid EMA
        value (seeded using the SMA of the first period).
        """

        if len(candles) < self.period:
            raise ValueError(
                "Not enough candles to calculate EMA."
            )

        closes = [candle.close for candle in candles]

        multiplier = 2 / (self.period + 1)

        sma = sum(closes[: self.period]) / self.period

        ema_values: list[float] = [sma]

        previous = sma

        for close in closes[self.period :]:
            current = (
                (close - previous) * multiplier
            ) + previous

            ema_values.append(current)

            previous = current

        return ema_values