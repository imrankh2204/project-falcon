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

from app.backtest.performance_snapshot import PerformanceSnapshot
from app.market.instrument import Instrument


@dataclass(frozen=True, slots=True)
class BacktestReport:
    """
    Immutable report representing a completed backtest.

    The report intentionally contains only presentation-facing metadata and
    immutable performance statistics. It is the canonical model consumed by
    report exporters and other presentation layers.

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
        Immutable snapshot of calculated performance statistics.
    """

    instrument: Instrument
    strategy_name: str

    start_time: datetime
    end_time: datetime

    performance: PerformanceSnapshot