"""
Portfolio aggregate root for Project Falcon.

Owns the active trading positions for a trading account.

Responsibilities:
    - Maintain active positions.
    - Enforce portfolio-level constraints.
    - Provide read-only access to portfolio state.

The Portfolio intentionally does NOT implement:

    - P&L calculations
    - Cash management
    - Position history
    - Exit lifecycle
    - Broker integration
    - Persistence
"""

from __future__ import annotations

from collections.abc import Mapping
from types import MappingProxyType

from app.trading.position import Position


class PortfolioError(Exception):
    """
    Raised when a portfolio operation violates a domain rule.
    """


class Portfolio:
    """
    Aggregate root representing the current trading account state.

    The Portfolio owns all active positions and enforces
    portfolio-level invariants.
    """

    def __init__(self) -> None:
        """
        Initialize an empty portfolio.
        """
        self._positions: dict[str, Position] = {}

    @property
    def positions(self) -> Mapping[str, Position]:
        """
        Return a read-only mapping of positions.

        Returns
        -------
        Mapping[str, Position]
            Immutable view of the portfolio positions.
        """
        return MappingProxyType(self._positions)

    @property
    def has_open_position(self) -> bool:
        """
        Return True when at least one position is open.
        """
        return any(position.is_open for position in self._positions.values())

    @property
    def open_position(self) -> Position | None:
        """
        Return the currently open position.

        Returns
        -------
        Position | None
            The active position if present, otherwise None.
        """
        for position in self._positions.values():
            if position.is_open:
                return position

        return None

    def add_position(self, position: Position) -> None:
        """
        Register a new position in the portfolio.

        Parameters
        ----------
        position:
            Position to register.

        Raises
        ------
        PortfolioError
            If:
                - object is not a Position
                - duplicate position id exists
                - another open position already exists
        """

        if not isinstance(position, Position):
            raise PortfolioError("Expected Position instance.")

        if position.position_id in self._positions:
            raise PortfolioError(
                f"Duplicate position id: {position.position_id}"
            )

        if self.has_open_position:
            raise PortfolioError(
                "Portfolio already contains an open position."
            )

        self._positions[position.position_id] = position