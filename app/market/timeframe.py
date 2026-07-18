"""
TimeFrame domain model for Project Falcon.

Defines all supported market timeframes used throughout
the Falcon trading framework.
"""

from __future__ import annotations

from enum import Enum


class TimeFrame(Enum):
    """
    Supported Falcon market timeframes.
    """

    ONE_MINUTE = "1m"
    THREE_MINUTES = "3m"
    FIVE_MINUTES = "5m"
    FIFTEEN_MINUTES = "15m"
    THIRTY_MINUTES = "30m"
    ONE_HOUR = "1h"
    FOUR_HOURS = "4h"
    ONE_DAY = "1d"

    def __str__(self) -> str:
        """
        Return the canonical timeframe string.
        """

        return self.value

    @classmethod
    def values(cls) -> list[str]:
        """
        Return all supported timeframe values.
        """

        return [item.value for item in cls]