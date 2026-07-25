"""
Optimization runner for Project Falcon.

This module provides deterministic orchestration of multiple backtest
executions across a parameter grid.

Responsibilities
----------------
- Iterate over parameter combinations.
- Create a BacktestApplication for each parameter set.
- Execute the application.
- Collect immutable optimization results.

The OptimizationRunner intentionally does NOT implement:

- Strategy construction
- Parameter generation
- Result ranking
- Parallel execution
- Report exporting
"""

from __future__ import annotations

from collections.abc import Callable

from app.backtest.optimization.parameter_grid import ParameterGrid
from app.backtest.optimization.result import OptimizationResult
from app.core.backtest_application import BacktestApplication
from app.strategies.ema_parameters import (
    EMACrossoverParameters,
)


class OptimizationRunner:
    """
    Deterministic optimization orchestrator.
    """

    def run(
        self,
        *,
        parameter_grid: ParameterGrid,
        application_factory: Callable[
            [EMACrossoverParameters],
            BacktestApplication,
        ],
    ) -> tuple[OptimizationResult, ...]:
        """
        Execute one backtest application for every valid parameter set.

        Parameters
        ----------
        parameter_grid
            Source of deterministic parameter combinations.

        application_factory
            Factory that builds a fully configured BacktestApplication
            for a supplied parameter set.

        Returns
        -------
        tuple[OptimizationResult, ...]
            Immutable optimization results preserving execution order.
        """

        results: list[OptimizationResult] = []

        for parameters in parameter_grid:

            application = application_factory(
                parameters
            )

            report = application.run()

            results.append(
                OptimizationResult(
                    parameters=parameters,
                    report=report,
                )
            )

        return tuple(results)