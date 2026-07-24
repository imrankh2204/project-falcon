"""
Console report exporter.

This module provides ConsoleExporter, responsible for converting an immutable
BacktestReport into a human-readable text representation suitable for terminal
output, logs, or other plain-text presentation layers.

The exporter performs formatting only. It contains no business logic,
calculations, persistence, or side effects.
"""

from __future__ import annotations

from app.backtest.reporting.exporter import ReportExporter
from app.backtest.reporting.report import BacktestReport


class ConsoleExporter(ReportExporter):
    """
    Serializes a BacktestReport into formatted console text.

    The exporter is deterministic and stateless. Numeric values are formatted
    for readability while preserving the underlying analytics supplied by the
    reporting model.
    """

    def export(self, report: BacktestReport) -> str:
        """
        Export a report as formatted plain text.

        Parameters
        ----------
        report
            Immutable report to serialize.

        Returns
        -------
        str
            Human-readable report.
        """

        performance = report.performance

        lines = [
            "=" * 60,
            "Project Falcon Backtest Report",
            "=" * 60,
            "",
            f"Strategy           : {report.strategy_name}",
            f"Instrument         : {report.instrument.symbol}",
            f"Start Time         : {report.start_time.isoformat(sep=' ')}",
            f"End Time           : {report.end_time.isoformat(sep=' ')}",
            "",
            "Performance",
            "-" * 60,
            f"Trade Count        : {performance.trade_count}",
            f"Winning Trades     : {performance.winning_trades}",
            f"Losing Trades      : {performance.losing_trades}",
            f"Win Rate           : {performance.win_rate:.2f}%",
            "",
            f"Gross Profit       : {performance.gross_profit:.2f}",
            f"Gross Loss         : {performance.gross_loss:.2f}",
            f"Net Profit         : {performance.net_profit:.2f}",
            "",
            f"Average Win        : {performance.average_win:.2f}",
            f"Average Loss       : {performance.average_loss:.2f}",
            "",
            f"Largest Win        : {performance.largest_win:.2f}",
            f"Largest Loss       : {performance.largest_loss:.2f}",
            "",
            "=" * 60,
        ]

        return "\n".join(lines)