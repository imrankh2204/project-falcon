"""
Portfolio aggregate root for Project Falcon.

Owns the trading positions for a trading account.

Responsibilities:
    - Maintain trading positions.
    - Enforce portfolio-level constraints.
    - Provide read-only access to portfolio state.
    - Aggregate portfolio accounting.
    - Expose portfolio analytics.

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
from app.trading.performance import PortfolioPerformance

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

    @property
    def win_rate(self) -> float:
        """
        Return the portfolio win rate as a percentage.

        Returns
        -------
        float
            Percentage of winning trades among all
            closed positions.

        Notes
        -----
        - Open positions are excluded.
        - Breakeven trades count as closed trades
          but not as winners.
        - Returns 0.0 when no closed positions exist.
        """
        if self.closed_position_count == 0:
            return 0.0

        return (
            self.winning_position_count
            / self.closed_position_count
        ) * 100.0

    def add_position(self, position: Position) -> None:
        """
        Register a new position in the portfolio.
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

    @property
    def average_winning_pnl(self) -> float:
        """
        Return the average realized profit of all winning positions.

        Returns
        -------
        float
            Average realized P&L of winning positions.
            Returns 0.0 when no winning positions exist.
        """

        winning_positions = [
            position
            for position in self._positions.values()
            if position.is_closed
            and position.realized_pnl > 0.0
        ]

        if not winning_positions:
            return 0.0

        total_profit = sum(
            position.realized_pnl
            for position in winning_positions
        )

        return total_profit / len(winning_positions)

    @property
    def average_losing_pnl(self) -> float:
        """
        Return the average realized loss of all losing positions.

        Returns
        -------
        float
            Average realized P&L of losing positions.
            Returns 0.0 when no losing positions exist.
        """

        losing_positions = [
            position
            for position in self._positions.values()
            if position.is_closed
            and position.realized_pnl < 0.0
        ]

        if not losing_positions:
            return 0.0

        total_loss = sum(
            position.realized_pnl
            for position in losing_positions
        )

        return total_loss / len(losing_positions)
    
    @property
    def profit_factor(self) -> float:
        """
        Return the portfolio profit factor.

        Profit Factor is defined as:

            Gross Winning P&L / Absolute Gross Losing P&L

        Returns
        -------
        float
            Portfolio profit factor.

            Returns:
                - float("inf") when no losing trades exist but at least
                  one winning trade exists.
                - 0.0 when no winning trades exist.
        """

        gross_profit = sum(
            position.realized_pnl
            for position in self._positions.values()
            if position.is_closed
            and position.realized_pnl > 0.0
        )

        gross_loss = abs(
            sum(
                position.realized_pnl
                for position in self._positions.values()
                if position.is_closed
                and position.realized_pnl < 0.0
            )
        )

        if gross_profit == 0.0:
            return 0.0

        if gross_loss == 0.0:
            return float("inf")

        return gross_profit / gross_loss
    
    @property
    def expectancy(self) -> float:
        """
        Return the portfolio expectancy.

        Expectancy is defined as:

            (Win Rate × Average Winning P&L)
            +
            (Loss Rate × Average Losing P&L)

        Returns
        -------
        float
            Expected realized P&L per completed trade.

            Returns 0.0 when no closed trades exist.
        """

        if self.closed_position_count == 0:
            return 0.0

        win_rate = (
            self.winning_position_count
            / self.closed_position_count
        )

        loss_rate = (
            self.losing_position_count
            / self.closed_position_count
        )

        return (
            (win_rate * self.average_winning_pnl)
            + (loss_rate * self.average_losing_pnl)
        )

    @property
    def performance(self) -> PortfolioPerformance:
        
        return PortfolioPerformance(
        total_realized_pnl=self.total_realized_pnl,

        closed_position_count=self.closed_position_count,
        winning_position_count=self.winning_position_count,
        losing_position_count=self.losing_position_count,
        breakeven_position_count=self.breakeven_position_count,

        win_rate=self.win_rate,

        average_winning_pnl=self.average_winning_pnl,
        average_losing_pnl=self.average_losing_pnl,

        profit_factor=self.profit_factor,

        expectancy=self.expectancy,
        )