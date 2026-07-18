"""
OptionType domain model for Project Falcon.

Defines supported option contract types.
"""

from __future__ import annotations

from enum import Enum


class OptionType(Enum):
    """
    Supported option contract types.
    """

    CALL = "CE"
    PUT = "PE"

    def __str__(self) -> str:
        return self.value

    @classmethod
    def values(cls) -> list[str]:
        """
        Return all supported option type values.
        """

        return [member.value for member in cls]