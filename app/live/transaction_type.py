"""
Broker-independent transaction type enumeration.

Defines the normalized transaction directions used throughout Falcon's
live trading layer.
"""

from __future__ import annotations

from enum import Enum


class TransactionType(str, Enum):
    """
    Immutable transaction direction.
    """

    BUY = "BUY"

    SELL = "SELL"