"""
Immutable streaming tick model.

Represents a broker-independent real-time market tick.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from app.market.instrument import Instrument


@dataclass(frozen=True, slots=True)
class Tick:
    """
    Immutable market tick.
    """

    instrument: Instrument

    price: float

    volume: float

    timestamp: datetime

    def __post_init__(self) -> None:

        if not isinstance(
            self.instrument,
            Instrument,
        ):
            raise TypeError(
                "instrument must be an Instrument."
            )

        if not isinstance(
            self.timestamp,
            datetime,
        ):
            raise TypeError(
                "timestamp must be a datetime."
            )

        if not isinstance(
            self.price,
            (int, float),
        ):
            raise TypeError(
                "price must be numeric."
            )

        if not isinstance(
            self.volume,
            (int, float),
        ):
            raise TypeError(
                "volume must be numeric."
            )

        if self.price < 0:
            raise ValueError(
                "price cannot be negative."
            )

        if self.volume < 0:
            raise ValueError(
                "volume cannot be negative."
            )