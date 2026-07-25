"""
Equity curve calculation for Project Falcon.

This module transforms completed trading positions into an immutable
equity curve representation.

Responsibilities
----------------
- Calculate chronological equity progression.
- Track peak equity.
- Calculate drawdown statistics.
- Produce EquityCurveSnapshot.

The EquityCurve calculator intentionally does NOT implement:

- Trade execution
- Portfolio management
- Strategy evaluation
- Replay orchestration
- Report exporting
"""

from __future__ import annotations

from collections.abc import Iterable

from app.backtest.equity_curve_snapshot import (
    EquityCurveSnapshot,
    EquityPoint,
)
from app.trading.position import Position


class EquityCurve:
    """
    Stateless utility for calculating equity progression.

    The calculator consumes completed positions only and converts
    realized P&L into a deterministic equity curve.
    """

    @staticmethod
    def calculate(
        positions: Iterable[Position],
        *,
        initial_capital: float = 0.0,
    ) -> EquityCurveSnapshot:
        """
        Calculate an equity curve from completed positions.

        Parameters
        ----------
        positions
            Iterable containing CLOSED trading positions.

        initial_capital
            Starting account equity.

        Returns
        -------
        EquityCurveSnapshot
            Immutable equity curve analysis.

        Raises
        ------
        ValueError
            If a supplied position is not closed.
        """

        if initial_capital < 0:
            raise ValueError(
                "initial_capital cannot be negative."
            )

        current_equity = initial_capital
        peak_equity = initial_capital

        maximum_drawdown = 0.0
        maximum_drawdown_percentage = 0.0

        points: list[EquityPoint] = []

        ordered_positions = sorted(
            positions,
            key=lambda position: (
                position.exit_time
                if position.exit_time is not None
                else position.entry_time
            ),
        )

        for position in ordered_positions:

            if not position.is_closed:
                raise ValueError(
                    "Equity curve requires closed positions only."
                )

            if position.exit_time is None:
                raise ValueError(
                    "Closed position must contain exit_time."
                )

            current_equity += position.realized_pnl

            points.append(
                EquityPoint(
                    timestamp=position.exit_time,
                    equity=current_equity,
                )
            )

            if current_equity > peak_equity:
                peak_equity = current_equity

            drawdown = peak_equity - current_equity

            if drawdown > maximum_drawdown:
                maximum_drawdown = drawdown

            if peak_equity > 0:
                drawdown_percentage = (
                    drawdown / peak_equity
                ) * 100.0
            else:
                drawdown_percentage = 0.0

            if (
                drawdown_percentage
                > maximum_drawdown_percentage
            ):
                maximum_drawdown_percentage = (
                    drawdown_percentage
                )

        return EquityCurveSnapshot(
            points=tuple(points),
            peak_equity=peak_equity,
            maximum_drawdown=maximum_drawdown,
            maximum_drawdown_percentage=(
                maximum_drawdown_percentage
            ),
        )