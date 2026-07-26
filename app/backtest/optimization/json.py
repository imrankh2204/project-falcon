"""
JSON exporter for Project Falcon optimization reports.

This module serializes immutable OptimizationReport objects into JSON.

Responsibilities
----------------
- Convert OptimizationReport into JSON.
- Produce deterministic output.
- Perform no filesystem operations.
"""

from __future__ import annotations

import json

from app.backtest.optimization.report import (
    OptimizationReport,
)


class OptimizationJsonExporter:
    """
    Serializes OptimizationReport objects into JSON text.
    """

    def export(
        self,
        report: OptimizationReport,
    ) ->str:
        """
        Serialize an optimization report to JSON.
        """

        if not isinstance(
            report,
            OptimizationReport,
        ):
            raise TypeError(
                "report must be an OptimizationReport."
            )

        data = []

        for result in report.results:

            performance = result.report.performance
            advanced = (
                result.report.advanced_performance
            )

            data.append(
                {
                    "fast_period": (
                        result.parameters.fast_period
                    ),
                    "slow_period": (
                        result.parameters.slow_period
                    ),
                    "net_profit": (
                        performance.net_profit
                    ),
                    "win_rate": (
                        performance.win_rate
                    ),
                    "profit_factor": (
                        advanced.profit_factor
                    ),
                }
            )

        return json.dumps(
            data,
            indent=4,
            sort_keys=True,
        )