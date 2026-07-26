"""
CSV exporter for Project Falcon optimization reports.

This module serializes immutable OptimizationReport objects into CSV.

Responsibilities
----------------
- Convert OptimizationReport into CSV.
- Produce deterministic output.
- Perform no filesystem operations.
"""

from __future__ import annotations

import csv
from io import StringIO

from app.backtest.optimization.report import (
    OptimizationReport,
)


class OptimizationCsvExporter:
    """
    Serializes OptimizationReport objects into CSV text.
    """

    def export(
        self,
        report: OptimizationReport,
    ) -> str:
        """
        Serialize an optimization report to CSV.
        """

        if not isinstance(
            report,
            OptimizationReport,
        ):
            raise TypeError(
                "report must be an OptimizationReport."
            )

        buffer = StringIO()

        writer = csv.writer(
            buffer,
            lineterminator="\n",
        )

        writer.writerow(
            (
                "fast_period",
                "slow_period",
                "net_profit",
                "win_rate",
                "profit_factor",
            )
        )

        for result in report.results:

            performance = result.report.performance
            advanced = result.report.advanced_performance

            writer.writerow(
                (
                    result.parameters.fast_period,
                    result.parameters.slow_period,
                    performance.net_profit,
                    performance.win_rate,
                    advanced.profit_factor,
                )
            )

        return buffer.getvalue()