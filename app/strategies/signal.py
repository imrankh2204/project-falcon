"""
Trading signal definitions for Project Falcon.
"""

from __future__ import annotations

from enum import Enum


class Signal(Enum):
    """
    Standard trading signals.
    """

    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"

    def __str__(self) -> str:
        return self.value