"""
Immutable optimization reporting model for Project Falcon.

This module defines the immutable reporting contract representing the
results of a completed optimization run.

The report is presentation-facing only and intentionally contains no
business logic, ranking logic, or calculations.

Responsibilities
----------------
- Store optimization results.
- Preserve deterministic ordering.
- Expose the selected optimization result.
- Provide an immutable reporting contract.

The report intentionally does NOT implement:

- Ranking algorithms
- Filtering
- Parameter generation
- Backtest execution
- Report rendering
"""

from __future__ import annotations

from dataclasses import dataclass

from app.backtest.optimization.result import OptimizationResult


@dataclass(frozen=True, slots=True)
class OptimizationReport:
    """
    Immutable optimization report.

    Attributes
    ----------
    results
        Optimization results in deterministic ranking order.
    """

    results: tuple[OptimizationResult, ...]

    def __post_init__(self) -> None:
        """
        Validate report contents.
        """

        for result in self.results:

            if not isinstance(
                result,
                OptimizationResult,
            ):
                raise TypeError(
                    "results must contain OptimizationResult objects."
                )

    @property
    def best_result(
        self,
    ) -> OptimizationResult:
        """
        Return the highest-ranked optimization result.

        Raises
        ------
        ValueError
            If the report contains no results.
        """

        if not self.results:
            raise ValueError(
                "OptimizationReport contains no results."
            )

        return self.results[0]

    @property
    def best_parameters(
        self,
    ):
        """
        Return the selected strategy parameters.
        """

        return self.best_result.parameters