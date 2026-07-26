"""
Optimization workflow orchestration for Project Falcon.

Coordinates execution of multiple optimization parameter configurations
through OptimizationExecutor and aggregates results into OptimizationReport.

Responsibilities
----------------
- Iterate optimization parameter sets.
- Execute isolated optimization runs.
- Collect OptimizationResult objects.
- Build final OptimizationReport.

The OptimizationWorkflow intentionally does NOT implement:

- Parameter generation
- Strategy creation
- Backtest execution
- Ranking
- Performance calculations
- Report presentation
"""

from __future__ import annotations

from app.backtest.optimization.report import (
    OptimizationReport,
)
from app.backtest.optimization.result import (
    OptimizationResult,
)
from app.strategies.ema_parameters import (
    EMACrossoverParameters,
)


class OptimizationWorkflow:
    """
    Coordinates complete optimization execution.

    The workflow is intentionally stateless. Every invocation of run()
    creates a deterministic OptimizationReport from the supplied parameter
    collection.
    """

    def __init__(
        self,
        *,
        executor,
        report_builder,
    ) -> None:

        if not callable(
            getattr(
                executor,
                "execute",
                None,
            )
        ):
            raise TypeError(
                "executor must provide an execute() method."
            )

        if not callable(
            getattr(
                report_builder,
                "build",
                None,
            )
        ):
            raise TypeError(
                "report_builder must provide a build() method."
            )

        self._executor = executor
        self._report_builder = report_builder

    def run(
        self,
        parameters: tuple[
            EMACrossoverParameters,
            ...,
        ],
    ) -> OptimizationReport:
        """
        Execute optimization workflow.

        Parameters
        ----------
        parameters
            Immutable collection of strategy parameter sets.

        Returns
        -------
        OptimizationReport
            Aggregated optimization report.

        Raises
        ------
        ValueError
            If no parameter sets are supplied.
        """

        if not isinstance(
            parameters,
            tuple,
        ):
            raise TypeError(
                "parameters must be a tuple."
            )

        if not parameters:
            raise ValueError(
                "Optimization requires at least one parameter set."
            )

        results: list[OptimizationResult] = []

        for parameter_set in parameters:

            result = self._executor.execute(
                parameter_set
            )

            results.append(
                result
            )

        return self._report_builder.build(
            tuple(results)
        )