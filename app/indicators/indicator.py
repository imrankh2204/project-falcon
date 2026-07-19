"""
Indicator abstraction for Project Falcon.

Defines the common interface implemented by all
technical indicators.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.market.candle import Candle


class Indicator(ABC):
    """
    Base class for all Falcon indicators.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Human-readable indicator name.
        """

    @abstractmethod
    def calculate(
        self,
        candles: list[Candle],
    ):
        """
        Calculate indicator values from a sequence of candles.
        """