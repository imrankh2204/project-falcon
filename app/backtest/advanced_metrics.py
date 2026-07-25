"""
Advanced performance analytics for Project Falcon.

This module provides stateless risk-adjusted performance calculations
derived from completed trading positions.

AdvancedPerformanceMetrics intentionally depends only on the Position
domain entity and produces an immutable AdvancedPerformanceSnapshot.

It does not depend on:

- Portfolio
- TradingService
- ReplayEngine
- Reporting components
- Persistence components
"""

from __future__ import annotations

from collections.abc import Iterable
from statistics import mean, pstdev

from app.backtest.advanced_performance_snapshot import (
    AdvancedPerformanceSnapshot,
)
from app.trading.position import Position


class AdvancedPerformanceMetrics:
    """
    Stateless utility for advanced backtest analytics.
    """

    @staticmethod
    def calculate(
        positions: Iterable[Position],
    ) -> AdvancedPerformanceSnapshot:
        """
        Calculate risk-adjusted performance statistics.

        Parameters
        ----------
        positions:
            Iterable of completed Position objects.

        Returns
        -------
        AdvancedPerformanceSnapshot
            Immutable advanced analytics result.
        """

        returns: list[float] = []

        gross_profit = 0.0
        gross_loss = 0.0

        winning_trades = 0
        losing_trades = 0

        for position in positions:

            if not position.is_closed:
                raise ValueError(
                    "Advanced metrics require closed positions only."
                )

            pnl = position.realized_pnl

            returns.append(pnl)

            if pnl > 0:
                winning_trades += 1
                gross_profit += pnl

            elif pnl < 0:
                losing_trades += 1
                gross_loss += abs(pnl)

        profit_factor = (
            gross_profit / gross_loss
            if gross_loss > 0
            else 0.0
        )

        expectancy = (
            AdvancedPerformanceMetrics
            ._calculate_expectancy(
                returns,
                winning_trades,
                losing_trades,
            )
        )

        sharpe_ratio = (
            AdvancedPerformanceMetrics
            ._calculate_sharpe(
                returns
            )
        )

        sortino_ratio = (
            AdvancedPerformanceMetrics
            ._calculate_sortino(
                returns
            )
        )

        return AdvancedPerformanceSnapshot(
            profit_factor=profit_factor,
            expectancy=expectancy,
            sharpe_ratio=sharpe_ratio,
            sortino_ratio=sortino_ratio,
        )

    @staticmethod
    def _calculate_expectancy(
        returns: list[float],
        winning_trades: int,
        losing_trades: int,
    ) -> float:
        """
        Calculate expected profit per trade.
        """

        total_trades = len(returns)

        if total_trades == 0:
            return 0.0

        average_win = (
            sum(
                value
                for value in returns
                if value > 0
            )
            / winning_trades
            if winning_trades > 0
            else 0.0
        )

        average_loss = (
            sum(
                abs(value)
                for value in returns
                if value < 0
            )
            / losing_trades
            if losing_trades > 0
            else 0.0
        )

        win_rate = (
            winning_trades / total_trades
        )

        loss_rate = (
            losing_trades / total_trades
        )

        return (
            (win_rate * average_win)
            -
            (loss_rate * average_loss)
        )

    @staticmethod
    def _calculate_sharpe(
        returns: list[float],
    ) -> float:
        """
        Calculate simplified trade-based Sharpe ratio.
        """

        if len(returns) < 2:
            return 0.0

        volatility = pstdev(returns)

        if volatility == 0:
            return 0.0

        return mean(returns) / volatility

    @staticmethod
    def _calculate_sortino(
        returns: list[float],
    ) -> float:
        """
        Calculate simplified trade-based Sortino ratio.
        """

        if not returns:
            return 0.0

        downside_returns = [
            value
            for value in returns
            if value < 0
        ]

        if not downside_returns:
            return 0.0

        downside_deviation = pstdev(
            downside_returns
        )

        if downside_deviation == 0:
            return 0.0

        return mean(returns) / downside_deviation