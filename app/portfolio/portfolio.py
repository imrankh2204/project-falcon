"""
Immutable Falcon portfolio aggregate.

Represents Falcon's internal portfolio state.

Responsibilities
----------------
- Own immutable portfolio positions.
- Provide deterministic portfolio snapshots.
- Remain broker independent.

The portfolio intentionally does NOT implement:

- Broker synchronization
- Position reconciliation
- Risk management
- P&L calculations
"""

from __future__ import annotations

from dataclasses import dataclass

from app.portfolio.portfolio_position import (
    PortfolioPosition,
)


@dataclass(frozen=True, slots=True)
class Portfolio:
    """
    Immutable portfolio aggregate.
    """

    positions: tuple[
        PortfolioPosition,
        ...,
    ] = ()

    def __post_init__(
        self,
    ) -> None:
        """
        Validate portfolio.
        """

        if not isinstance(
            self.positions,
            tuple,
        ):
            raise TypeError(
                "positions must be a tuple."
            )

        for position in self.positions:
            if not isinstance(
                position,
                PortfolioPosition,
            ):
                raise TypeError(
                    "positions must contain "
                    "PortfolioPosition objects."
                )

    @property
    def total_positions(
        self,
    ) -> int:
        """
        Return the number of positions.
        """

        return len(
            self.positions,
        )

    @staticmethod
    def empty(
    ) -> "Portfolio":
        """
        Return an empty portfolio.
        """

        return Portfolio()