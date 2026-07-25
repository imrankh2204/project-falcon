"""
Immutable backtest result model.

This module defines BacktestResult, the immutable output of a completed
backtest session. It aggregates the execution context together with the
computed performance statistics while remaining independent of replay,
trading, and persistence implementations.
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
class BacktestResult:
    """
    Immutable representation of a completed backtest.

    Attributes
    ----------
    instrument
        Instrument used for the backtest.

    strategy_name
        Name of the strategy that produced the result.

    start_time
        Timestamp of the first replayed candle.

    end_time
        Timestamp of the final replayed candle.

    performance
        Basic performance statistics.

    advanced_performance
        Advanced performance analytics.

    equity_curve
        Immutable equity curve analytics.
    """

    instrument: Instrument

    strategy_name: str

    start_time: datetime | None

    end_time: datetime | None

    performance: PerformanceSnapshot

    advanced_performance: AdvancedPerformanceSnapshot

    equity_curve: EquityCurveSnapshot