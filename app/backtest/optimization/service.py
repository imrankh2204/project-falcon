"""
Optimization service for Project Falcon.

This module provides the public orchestration layer for optimization
execution.

Responsibilities
----------------
- Build parameter grid from configuration.
- Execute optimization workflow.
- Return immutable OptimizationReport.

The OptimizationService intentionally does NOT implement:

- Strategy construction
- Backtest execution
- Ranking
- Report exporting
- Console formatting
"""

from __future__ import annotations

from app.backtest.optimization.config import (
    OptimizationConfig,
)
from app.backtest.optimization.parameter_grid import (
    ParameterGrid,
)
from app.backtest.optimization.report import (
    OptimizationReport,
)
from app.backtest.optimization.workflow import (
    OptimizationWorkflow,
)


class OptimizationService:
    """
    Public orchestration service for optimization execution.
    """

    def __init__(
        self,
        *,
        workflow: OptimizationWorkflow,
    ) -> None:

        if not isinstance(
            workflow,
            OptimizationWorkflow,
        ):
            raise TypeError(
                "workflow must be an OptimizationWorkflow."
            )

        self._workflow = workflow

    def run(
        self,
        config: OptimizationConfig,
    ) -> OptimizationReport:
        """
        Execute optimization using the supplied configuration.
        """

        if not isinstance(
            config,
            OptimizationConfig,
        ):
            raise TypeError(
                "config must be an OptimizationConfig."
            )

        grid = ParameterGrid(
            fast_periods=config.fast_periods,
            slow_periods=config.slow_periods,
        )

        parameters = tuple(grid)

        if (
            config.max_combinations
            is not None
        ):
            parameters = parameters[
                : config.max_combinations
            ]

        return self._workflow.run(
            parameters
        )