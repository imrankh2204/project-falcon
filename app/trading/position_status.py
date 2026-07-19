"""
Position status definitions for Project Falcon.
"""

from __future__ import annotations

from enum import Enum


class PositionStatus(Enum):
    """
    Represents the lifecycle state of a position.
    """

    OPEN = "OPEN"
    CLOSED = "CLOSED"

    def __str__(self) -> str:
        return self.value