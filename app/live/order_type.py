"""
Broker-independent order type enumeration.

Defines the normalized order types supported by Falcon's live trading
layer regardless of the underlying broker implementation.
"""

from __future__ import annotations

from enum import Enum


class OrderType(str, Enum):
    """
    Immutable broker order type.
    """

    MARKET = "MARKET"

    LIMIT = "LIMIT"

    SL = "SL"

    SL_MARKET = "SL_MARKET"