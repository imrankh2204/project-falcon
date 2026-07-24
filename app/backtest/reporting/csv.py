"""
CSV report exporter.

This module provides CsvExporter, responsible for serializing immutable
BacktestReport instances into CSV format.

The exporter performs serialization only. It contains no business logic,
calculations, persistence, or side effects.
"""

from __future__ import annotations

import csv
from io import StringIO

from app.backtest.reporting.exporter import ReportExporter
from app.backtest.reporting.report import BacktestReport


class CsvExporter(ReportExporter):
    """
    Serializes a BacktestReport into CSV.

    The exporter is deterministic and always emits the same header order.
    One report corresponds to exactly one CSV record.
    """

    _HEADERS = (
        "strategy_name",
        "instrument",
        "start_time",
        "end_time",
        "trade_count",
        "winning_trades",
        "losing_trades",
        "win_rate",
        "gross_profit",
        "gross_loss",
        "net_profit",
        "average_win",
        "average_loss",
        "largest_win",
        "largest_loss",
    )

    def export(self, report: BacktestReport) -> str:
        """
        Serialize a report into CSV.

        Parameters
        ----------
        report
            Immutable report to serialize.

        Returns
        -------
        str
            CSV representation containing a header row and one data row.
        """

        performance = report.performance

        buffer = StringIO()
        writer = csv.writer(buffer, lineterminator="\n")

        writer.writerow(self._HEADERS)

        writer.writerow(
            (
                report.strategy_name,
                report.instrument.symbol,
                report.start_time.isoformat(),
                report.end_time.isoformat(),
                performance.trade_count,
                performance.winning_trades,
                performance.losing_trades,
                performance.win_rate,
                performance.gross_profit,
                performance.gross_loss,
                performance.net_profit,
                performance.average_win,
                performance.average_loss,
                performance.largest_win,
                performance.largest_loss,
            )
        )

        return buffer.getvalue()