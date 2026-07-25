"""
Performance metrics computation for Project Falcon.

This module provides a stateless computation utility that transforms a
read-only collection of completed trading positions into an immutable
PerformanceSnapshot.

PerformanceMetrics intentionally depends only on the Position domain
entity and optional ExecutionCostModel. It does not depend on Portfolio,
TradingService, ReplayEngine, or persistence components.
"""

from __future__ import annotations

from collections.abc import Iterable

from app.backtest.execution_cost_model import ExecutionCostModel
from app.backtest.performance_snapshot import PerformanceSnapshot
from app.trading.position import Position


class PerformanceMetrics:
    """
    Stateless utility for calculating backtest performance statistics.
    """

    @staticmethod
    def calculate(
        positions: Iterable[Position],
        execution_cost_model: ExecutionCostModel | None = None,
    ) -> PerformanceSnapshot:
        """
        Calculate performance statistics from completed positions.

        Parameters
        ----------
        positions
            Read-only iterable of CLOSED Position objects.

        execution_cost_model
            Optional execution cost model used to deduct transaction
            costs from realized profit and loss.

        Returns
        -------
        PerformanceSnapshot
            Immutable summary of computed performance statistics.

        Raises
        ------
        ValueError
            If any supplied position is not closed.
        """

        trade_count = 0

        winning_trades = 0
        losing_trades = 0

        gross_profit = 0.0
        gross_loss = 0.0

        largest_win = 0.0
        largest_loss = 0.0

        for position in positions:

            if not position.is_closed:
                raise ValueError(
                    "Performance metrics require closed positions only."
                )

            trade_count += 1

            pnl = position.realized_pnl

            #
            # Deduct execution costs when configured.
            #

            if execution_cost_model is not None:

                pnl -= execution_cost_model.total_cost(
                    quantity=position.quantity,
                )

            if pnl > 0:

                winning_trades += 1
                gross_profit += pnl

                if pnl > largest_win:
                    largest_win = pnl

            elif pnl < 0:

                loss = abs(pnl)

                losing_trades += 1
                gross_loss += loss

                if loss > largest_loss:
                    largest_loss = loss

        net_profit = gross_profit - gross_loss

        win_rate = (
            (winning_trades / trade_count) * 100.0
            if trade_count > 0
            else 0.0
        )

        average_win = (
            gross_profit / winning_trades
            if winning_trades > 0
            else 0.0
        )

        average_loss = (
            gross_loss / losing_trades
            if losing_trades > 0
            else 0.0
        )

        return PerformanceSnapshot(
            trade_count=trade_count,
            winning_trades=winning_trades,
            losing_trades=losing_trades,
            win_rate=win_rate,
            gross_profit=gross_profit,
            gross_loss=gross_loss,
            net_profit=net_profit,
            average_win=average_win,
            average_loss=average_loss,
            largest_win=largest_win,
            largest_loss=largest_loss,
        )