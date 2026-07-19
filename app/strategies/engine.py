"""
Strategy execution engine for Project Falcon.
"""

from __future__ import annotations

from app.strategies.context import StrategyContext
from app.strategies.signal import Signal
from app.strategies.strategy import Strategy


class StrategyEngine:
    """
    Executes one or more trading strategies.
    """

    def __init__(
        self,
        strategies: list[Strategy],
    ) -> None:

        self._strategies = strategies

    @property
    def strategy_count(self) -> int:
        """
        Number of registered strategies.
        """

        return len(self._strategies)

    def evaluate(
        self,
        context: StrategyContext,
    ) -> dict[str, Signal]:
        """
        Execute every registered strategy.
        """

        results: dict[str, Signal] = {}

        for strategy in self._strategies:
            results[strategy.name] = strategy.evaluate(context)

        return results