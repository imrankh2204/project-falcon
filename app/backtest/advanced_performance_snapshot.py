"""
Immutable advanced performance analytics snapshot.

This module defines the value object returned by
AdvancedPerformanceMetrics.

The snapshot contains risk-adjusted performance statistics
calculated from completed backtest trades.

The object contains no calculation logic and exists only as
an immutable transport model between analytics and reporting.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AdvancedPerformanceSnapshot:
    """
    Immutable advanced performance statistics.

    Attributes
    ----------
    profit_factor
        Ratio of gross profits to gross losses.

    expectancy
        Expected profit or loss per trade.

    sharpe_ratio
        Return-to-volatility measurement.

    sortino_ratio
        Return-to-downside-volatility measurement.
    """

    profit_factor: float

    expectancy: float

    sharpe_ratio: float

    sortino_ratio: float