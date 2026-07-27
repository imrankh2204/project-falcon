"""
Broker-independent order status enumeration.

Defines the normalized order lifecycle used throughout Falcon's live
trading layer regardless of the underlying broker implementation.
"""

from __future__ import annotations

from enum import Enum


class OrderStatus(str, Enum):
    """
    Immutable broker order status.
    """

    NEW = "NEW"

    OPEN = "OPEN"

    PARTIALLY_FILLED = "PARTIALLY_FILLED"

    FILLED = "FILLED"

    CANCELLED = "CANCELLED"

    REJECTED = "REJECTED"

    EXPIRED = "EXPIRED"