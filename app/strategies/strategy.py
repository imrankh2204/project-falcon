"""
Strategy abstraction for Project Falcon.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.strategies.context import StrategyContext
from app.strategies.signal import Signal


class Strategy(ABC):
    """
    Base class for all Falcon trading strategies.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Human-readable strategy name.
        """

    @abstractmethod
    def evaluate(
        self,
        context: StrategyContext,
    ) -> Signal:
        """
        Evaluate market conditions and return a trading signal.
        """