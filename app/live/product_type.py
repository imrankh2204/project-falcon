"""
Broker-independent product type enumeration.

Defines the normalized product classifications used by Falcon's live
trading layer.

The enumeration intentionally remains broker-agnostic while supporting
the common intraday and carry-forward product categories.
"""

from __future__ import annotations

from enum import Enum


class ProductType(str, Enum):
    """
    Immutable broker product type.
    """

    MIS = "MIS"

    NRML = "NRML"

    CNC = "CNC"