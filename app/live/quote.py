"""
Immutable market quote model.

Represents a normalized broker-independent market quote snapshot.

Responsibilities
----------------
- Hold the latest bid/ask information.
- Preserve immutable market state.
- Remain broker agnostic.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from app.market.instrument import Instrument


@dataclass(frozen=True, slots=True)
class Quote:
    """
    Immutable market quote.
    """

    instrument: Instrument

    last_price: float

    bid: float

    ask: float

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

        for name, value in (
            ("last_price", self.last_price),
            ("bid", self.bid),
            ("ask", self.ask),
            ("volume", self.volume),
        ):
            if not isinstance(
                value,
                (int, float),
            ):
                raise TypeError(
                    f"{name} must be numeric."
                )

        if self.last_price < 0:
            raise ValueError(
                "last_price cannot be negative."
            )

        if self.bid < 0:
            raise ValueError(
                "bid cannot be negative."
            )

        if self.ask < 0:
            raise ValueError(
                "ask cannot be negative."
            )

        if self.volume < 0:
            raise ValueError(
                "volume cannot be negative."
            )