"""
Report builder for completed backtests.
"""

from __future__ import annotations

from app.backtest.backtest_result import BacktestResult
from app.backtest.reporting.report import BacktestReport


class ReportBuilder:
    """
    Builds immutable reporting models from completed backtest results.
    """

    def build(
        self,
        result: BacktestResult,
    ) -> BacktestReport:

        return BacktestReport(
            instrument=result.instrument,
            strategy_name=result.strategy_name,
            start_time=result.start_time,
            end_time=result.end_time,
            performance=result.performance,
            advanced_performance=(
                result.advanced_performance
            ),
            equity_curve=result.equity_curve,
        )