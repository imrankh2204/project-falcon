"""
Strategy context for Project Falcon.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.market.candle import Candle
from app.market.instrument import Instrument
from app.market.timeframe import TimeFrame


@dataclass(slots=True)
class StrategyContext:
    """
    Input supplied to every trading strategy.
    """

    instrument: Instrument
    timeframe: TimeFrame
    candles: list[Candle]