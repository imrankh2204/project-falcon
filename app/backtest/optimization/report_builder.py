"""
Optimization report builder for Project Falcon.

Transforms optimization results into the immutable reporting model.

The builder performs no calculations, ranking, filtering, or formatting.
Its sole responsibility is constructing an immutable OptimizationReport
while preserving deterministic ordering.
"""

from __future__ import annotations

from app.backtest.optimization.report import OptimizationReport
from app.backtest.optimization.result import OptimizationResult


class OptimizationReportBuilder:
    """
    Stateless builder for immutable optimization reports.
    """

    def build(
        self,
        results: tuple[OptimizationResult, ...],
    ) -> OptimizationReport:
        """
        Build an immutable optimization report.

        Parameters
        ----------
        results
            Optimization results in deterministic execution order.

        Returns
        -------
        OptimizationReport
            Immutable optimization report.
        """

        return OptimizationReport(
            results=tuple(results),
        )