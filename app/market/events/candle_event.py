"""
Project Falcon

Candle Event

Represents a completed market candle
received by the runtime.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.market.candle import Candle

from app.market.events.market_event import MarketEvent


@dataclass(
    frozen=True,
)
class CandleEvent(MarketEvent):
    """
    Market event containing candle data.
    """

    candle: Candle