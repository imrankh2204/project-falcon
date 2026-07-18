"""
Instrument domain model for Project Falcon.

Represents a tradable financial instrument.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from app.market.option_type import OptionType


@dataclass(frozen=True, slots=True)
class Instrument:
    """
    Tradable market instrument.
    """

    exchange: str
    symbol: str
    instrument_token: int
    lot_size: int
    tick_size: float

    expiry: date | None = None
    strike: float | None = None
    option_type: OptionType | None = None

    @property
    def is_option(self) -> bool:
        """
        True if this instrument is an option contract.
        """
        return self.option_type is not None

    @property
    def display_name(self) -> str:
        """
        Human-readable instrument name.
        """
        return f"{self.exchange}:{self.symbol}"