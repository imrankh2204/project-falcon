"""
Optimization ranking engine for Project Falcon.

Provides deterministic ordering of optimization results.

Responsibilities
----------------
- Rank optimization results.
- Preserve deterministic ordering.

The RankingEngine intentionally does NOT implement:

- Backtest execution
- Parameter generation
- Report rendering
- Performance calculations
"""

from __future__ import annotations

from enum import Enum, auto

from app.backtest.optimization.report import OptimizationReport
from app.backtest.optimization.result import OptimizationResult


class RankingMetric(Enum):
    """
    Supported optimization ranking metrics.
    """

    NET_PROFIT = auto()
    WIN_RATE = auto()
    PROFIT_FACTOR = auto()


class RankingEngine:
    """
    Stateless deterministic ranking engine.
    """

    def rank(
        self,
        report: OptimizationReport,
        metric: RankingMetric,
    ) -> tuple[OptimizationResult, ...]:
        """
        Rank optimization results.
        """

        return tuple(
            sorted(
                report.results,
                key=lambda result: (
                    self._metric_value(
                        result,
                        metric,
                    )
                ),
                reverse=True,
            )
        )

    @staticmethod
    def _metric_value(
        result: OptimizationResult,
        metric: RankingMetric,
    ) -> float:
        """
        Extract ranking value from nested report.
        """

        performance = result.report.performance

        if metric is RankingMetric.NET_PROFIT:
            return performance.net_profit

        if metric is RankingMetric.WIN_RATE:
            return performance.win_rate

        if metric is RankingMetric.PROFIT_FACTOR:
            advanced_performance = (
                result.report.advanced_performance
            )
            
            if advanced_performance is None:
                return 0.0

            return (
                advanced_performance.profit_factor
            )

        raise ValueError(
            f"Unsupported ranking metric: {metric!r}"
        )