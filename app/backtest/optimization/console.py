"""
Optimization console exporter for Project Falcon.

Provides human-readable console formatting for optimization reports.

This module is responsible only for presentation formatting.

Responsibilities
----------------
- Render optimization results.
- Produce deterministic console output.

The OptimizationConsoleExporter intentionally does NOT implement:

- Ranking
- Filtering
- Optimization execution
- Performance calculations
"""

from __future__ import annotations

from app.backtest.optimization.report import (
    OptimizationReport,
)


class OptimizationConsoleExporter:
    """
    Stateless console exporter for optimization reports.
    """

    def export(
        self,
        report: OptimizationReport,
    ) -> str:
        """
        Export optimization report.

        Parameters
        ----------
        report
            Immutable optimization report.

        Returns
        -------
        str
            Human-readable optimization report.
        """

        lines: list[str] = []

        lines.append("=" * 60)
        lines.append(
            "Project Falcon Optimization Report"
        )
        lines.append("=" * 60)
        lines.append("")

        for index, result in enumerate(
            report.results,
            start=1,
        ):

            performance = (
                result.report.performance
            )

            advanced_performance = (
                result.report.advanced_performance
            )

            lines.append(
                f"Rank               : {index}"
            )

            lines.append(
                f"Parameters         : "
                f"{result.parameters}"
            )

            lines.append(
                f"Net Profit         : "
                f"{performance.net_profit:.2f}"
            )

            lines.append(
                f"Win Rate           : "
                f"{performance.win_rate:.2f}%"
            )

            if advanced_performance is not None:
                lines.append(
                    f"Profit Factor      : "
                    f"{advanced_performance.profit_factor:.2f}"
                )

            else:
                lines.append(
                    "Profit Factor      : 0.00"
                )

            lines.append("")

        lines.append("=" * 60)

        return "\n".join(lines)