"""
Immutable reporting model for completed backtests.

This module defines BacktestReport, the public reporting contract exposed by
the reporting subsystem. The report contains only business-facing information
required by presentation layers and remains completely independent from the
backtesting engine implementation.

The object is immutable to guarantee deterministic behaviour and to ensure
that exported reports always represent a stable snapshot of a completed
backtest.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from app.backtest.advanced_performance_snapshot import (
    AdvancedPerformanceSnapshot,
)
from app.backtest.equity_curve_snapshot import (
    EquityCurveSnapshot,
)
from app.backtest.performance_snapshot import (
    PerformanceSnapshot,
)
from app.market.instrument import Instrument


@dataclass(frozen=True, slots=True)
class BacktestReport:
    """
    Immutable report representing a completed backtest.

    Attributes
    ----------
    instrument
        Instrument used for the backtest.

    strategy_name
        Name of the evaluated trading strategy.

    start_time
        Timestamp of the first replayed candle.

    end_time
        Timestamp of the final replayed candle.

    performance
        Core performance statistics.

    advanced_performance
        Risk-adjusted performance analytics.

    equity_curve
        Immutable equity curve statistics.
    """

    instrument: Instrument
    strategy_name: str

    start_time: datetime | None
    end_time: datetime | None

    performance: PerformanceSnapshot

    advanced_performance: AdvancedPerformanceSnapshot

    equity_curve: EquityCurveSnapshot