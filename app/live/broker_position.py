"""
Immutable broker position model.

Represents a normalized snapshot of an open broker position.

Responsibilities
----------------
- Hold broker-reported position information.
- Remain broker independent.
- Provide immutable transport semantics.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.market.instrument import Instrument


@dataclass(frozen=True, slots=True)
class BrokerPosition:
    """
    Immutable broker position snapshot.
    """

    instrument: Instrument

    quantity: int

    average_price: float

    realized_pnl: float

    unrealized_pnl: float

    def __post_init__(self) -> None:

        if not isinstance(
            self.instrument,
            Instrument,
        ):
            raise TypeError(
                "instrument must be an Instrument."
            )

        if not isinstance(
            self.quantity,
            int,
        ):
            raise TypeError(
                "quantity must be an integer."
            )

        if self.quantity < 0:
            raise ValueError(
                "quantity cannot be negative."
            )

        for name, value in (
            ("average_price", self.average_price),
            ("realized_pnl", self.realized_pnl),
            ("unrealized_pnl", self.unrealized_pnl),
        ):
            if not isinstance(
                value,
                (int, float),
            ):
                raise TypeError(
                    f"{name} must be numeric."
                )

        if self.average_price < 0:
            raise ValueError(
                "average_price cannot be negative."
            )