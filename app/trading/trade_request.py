"""
Trade request model for Project Falcon.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.market.instrument import Instrument
from app.strategies.signal import Signal


@dataclass(slots=True)
class TradeRequest:
    """
    Represents a strategy's intent to trade.

    This object is broker-independent and is evaluated by
    the RiskManager before reaching any execution engine.
    """

    instrument: Instrument
    signal: Signal
    quantity: int