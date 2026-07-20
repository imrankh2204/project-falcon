"""
Portfolio aggregate root for Project Falcon.

Owns the trading positions for a trading account.

Responsibilities:
    - Maintain trading positions.
    - Enforce portfolio-level constraints.
    - Provide read-only access to portfolio state.
    - Aggregate portfolio accounting.

The Portfolio intentionally does NOT implement:

    - Trade-level P&L calculations
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

    The Portfolio owns all trading positions and exposes
    portfolio-level aggregate information.
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
        """
        return MappingProxyType(self._positions)

    @property
    def has_open_position(self) -> bool:
        """
        Return True when at least one position is open.
        """
        return any(
            position.is_open
            for position in self._positions.values()
        )

    @property
    def open_position(self) -> Position | None:
        """
        Return the currently open position.
        """
        for position in self._positions.values():
            if position.is_open:
                return position

        return None

    @property
    def total_realized_pnl(self) -> float:
        """
        Return total realized portfolio P&L.

        Only closed positions contribute.
        """
        return sum(
            position.realized_pnl
            for position in self._positions.values()
            if position.is_closed
        )

    @property
    def closed_position_count(self) -> int:
        """
        Return the number of closed positions.
        """
        return sum(
            1
            for position in self._positions.values()
            if position.is_closed
        )

    @property
    def winning_position_count(self) -> int:
        """
        Return the number of profitable closed positions.
        """
        return sum(
            1
            for position in self._positions.values()
            if position.is_closed
            and position.realized_pnl > 0
        )

    @property
    def losing_position_count(self) -> int:
        """
        Return the number of losing closed positions.
        """
        return sum(
            1
            for position in self._positions.values()
            if position.is_closed
            and position.realized_pnl < 0
        )

    @property
    def breakeven_position_count(self) -> int:
        """
        Return the number of breakeven closed positions.
        """
        return sum(
            1
            for position in self._positions.values()
            if position.is_closed
            and position.realized_pnl == 0
        )

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
            raise PortfolioError(
                "Expected Position instance."
            )

        if position.position_id in self._positions:
            raise PortfolioError(
                f"Duplicate position id: {position.position_id}"
            )

        if self.has_open_position:
            raise PortfolioError(
                "Portfolio already contains an open position."
            )

        self._positions[position.position_id] = position