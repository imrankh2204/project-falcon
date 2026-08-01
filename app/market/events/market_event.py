"""
Project Falcon

Market Event Contract

Defines the base abstraction for all runtime
market data events.
"""

from __future__ import annotations

from abc import ABC


class MarketEvent(ABC):
    """
    Base class for market events.

    Examples:
    - CandleEvent
    - TickEvent (future)
    """

    pass