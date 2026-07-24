"""
Report builder for completed backtests.

This module defines ReportBuilder, responsible for transforming the immutable
BacktestResult produced by the backtesting pipeline into the immutable
BacktestReport consumed by the reporting subsystem.

The builder performs no calculations and contains no business logic. All
performance statistics are expected to have been computed upstream by
PerformanceMetrics and exposed through PerformanceSnapshot.
"""

from __future__ import annotations

from app.backtest.backtest_result import BacktestResult
from app.backtest.reporting.report import BacktestReport


class ReportBuilder:
    """
    Builds immutable reporting models from completed backtest results.

    ReportBuilder is intentionally stateless and deterministic. Its sole
    responsibility is to translate the execution-facing BacktestResult into
    the presentation-facing BacktestReport.
    """

    def build(self, result: BacktestResult) -> BacktestReport:
        """
        Build a reporting model from a completed backtest.

        Parameters
        ----------
        result
            Immutable backtest result produced by the replay pipeline.

        Returns
        -------
        BacktestReport
            Immutable report suitable for serialization and presentation.
        """

        return BacktestReport(
            instrument=result.instrument,
            strategy_name=result.strategy_name,
            start_time=result.start_time,
            end_time=result.end_time,
            performance=result.performance,
        )