"""
EMA Crossover strategy for Project Falcon.
"""

from __future__ import annotations

from app.indicators.ema import EMA
from app.strategies.context import StrategyContext
from app.strategies.signal import Signal
from app.strategies.strategy import Strategy


class EMACrossoverStrategy(Strategy):
    """
    Fast EMA / Slow EMA crossover strategy.
    """

    def __init__(
        self,
        fast_period: int = 9,
        slow_period: int = 21,
    ) -> None:

        if fast_period >= slow_period:
            raise ValueError(
                "fast_period must be less than slow_period."
            )

        self._fast = EMA(fast_period)
        self._slow = EMA(slow_period)

    @property
    def name(self) -> str:
        return (
            f"EMA Crossover "
            f"({self._fast.period}/{self._slow.period})"
        )

    def evaluate(
        self,
        context: StrategyContext,
    ) -> Signal:

        candles = context.candles

        if len(candles) < self._slow.period + 1:
            return Signal.HOLD

        fast = self._fast.calculate(candles)
        slow = self._slow.calculate(candles)

        offset = self._slow.period - self._fast.period

        fast = fast[offset:]

        previous_fast = fast[-2]
        current_fast = fast[-1]

        previous_slow = slow[-2]
        current_slow = slow[-1]

        if (
            previous_fast <= previous_slow
            and current_fast > current_slow
        ):
            return Signal.BUY

        if (
            previous_fast >= previous_slow
            and current_fast < current_slow
        ):
            return Signal.SELL

        return Signal.HOLD