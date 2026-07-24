"""
Immutable performance statistics produced by a completed backtest.

This module defines PerformanceSnapshot, a lightweight value object that
captures summary statistics calculated from completed trades. The snapshot
contains no business logic and is intended to be created exclusively by
PerformanceMetrics.

The object is immutable to ensure deterministic behaviour throughout the
backtesting pipeline and to prevent accidental mutation after calculation.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PerformanceSnapshot:
    """
    Immutable summary of backtest performance.

    All monetary values are expressed using the project's configured currency
    units. Gross loss is represented as a positive magnitude, while net profit
    is the signed overall result.

    Attributes
    ----------
    trade_count
        Total number of completed trades.

    winning_trades
        Number of profitable completed trades.

    losing_trades
        Number of losing completed trades.

    win_rate
        Percentage of winning trades expressed as a value between
        0.0 and 100.0.

    gross_profit
        Sum of profits from all winning trades.

    gross_loss
        Sum of losses from all losing trades, expressed as a positive value.

    net_profit
        Overall signed profit or loss.

    average_win
        Average profit across winning trades.

    average_loss
        Average loss across losing trades, expressed as a positive value.

    largest_win
        Largest individual trade profit.

    largest_loss
        Largest individual trade loss, expressed as a positive value.
    """

    trade_count: int
    winning_trades: int
    losing_trades: int

    win_rate: float

    gross_profit: float
    gross_loss: float
    net_profit: float

    average_win: float
    average_loss: float

    largest_win: float
    largest_loss: float