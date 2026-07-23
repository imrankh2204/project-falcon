"""
Analytics result domain model for Project Falcon.

Represents an immutable snapshot of calculated portfolio
analytics metrics.

Responsibilities:
    - Store calculated analytics values.
    - Provide a stable contract between analytics calculation
      and future consumers.

The AnalyticsResult intentionally does NOT implement:

    - Metric calculation
    - Portfolio access
    - Trade execution
    - Data loading
    - Reporting or visualization
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AnalyticsResult:
    """
    Immutable analytics calculation result.

    Represents calculated performance metrics derived from a
    portfolio state.

    Attributes
    ----------
    total_trades:
        Total number of completed trades.

    winning_trades:
        Number of trades with positive realized PnL.

    losing_trades:
        Number of trades with negative realized PnL.

    win_rate:
        Ratio of winning trades to total trades.

    net_pnl:
        Total realized profit and loss.

    average_win:
        Average PnL of winning trades.

    average_loss:
        Average PnL of losing trades.
    """

    total_trades: int
    winning_trades: int
    losing_trades: int
    win_rate: float
    net_pnl: float
    average_win: float
    average_loss: float