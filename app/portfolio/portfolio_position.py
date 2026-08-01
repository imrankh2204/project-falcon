"""
Immutable Falcon portfolio position.

Represents Falcon's internal view of an active trading position.

Unlike BrokerPosition, this model belongs to the portfolio domain and
is independent of any specific broker implementation.

Responsibilities
----------------
- Store immutable portfolio position information.
- Remain broker independent.
- Provide deterministic portfolio state.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.market.instrument import Instrument


@dataclass(frozen=True, slots=True)
class PortfolioPosition:
    """
    Immutable portfolio position.
    """

    instrument: Instrument

    quantity: int

    average_price: float

    realized_pnl: float

    unrealized_pnl: float

    def __post_init__(
        self,
    ) -> None:
        """
        Validate the portfolio position.
        """

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
            (
                "average_price",
                self.average_price,
            ),
            (
                "realized_pnl",
                self.realized_pnl,
            ),
            (
                "unrealized_pnl",
                self.unrealized_pnl,
            ),
        ):
            if not isinstance(
                value,
                (
                    int,
                    float,
                ),
            ):
                raise TypeError(
                    f"{name} must be numeric."
                )

        if self.average_price < 0:
            raise ValueError(
                "average_price cannot be negative."
            )