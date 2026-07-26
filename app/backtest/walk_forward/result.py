"""
Immutable walk-forward optimization results.

This module defines value objects representing completed
walk-forward optimization evaluations.

Responsibilities
----------------
- Store individual walk-forward iteration results.
- Store aggregate walk-forward execution results.
- Provide immutable transport models.

The result models intentionally do NOT implement:

- Optimization execution
- Backtest execution
- Ranking
- Metric calculations
- Exporting
"""

from __future__ import annotations

from dataclasses import dataclass

from app.backtest.optimization.result import (
    OptimizationResult,
)
from app.backtest.walk_forward.window import (
    WalkForwardWindow,
)


@dataclass(frozen=True, slots=True)
class WalkForwardIterationResult:
    """
    Immutable result for a single walk-forward iteration.

    Attributes
    ----------
    window
        Training and validation period definition.

    optimization_result
        Result produced from training window optimization.

    validation_report
        Backtest report produced from validation window execution.
    """

    window: WalkForwardWindow

    optimization_result: OptimizationResult

    validation_report: object

    def __post_init__(self) -> None:
        """
        Validate iteration result dependencies.
        """

        if not isinstance(
            self.window,
            WalkForwardWindow,
        ):
            raise TypeError(
                "window must be a WalkForwardWindow."
            )

        if not isinstance(
            self.optimization_result,
            OptimizationResult,
        ):
            raise TypeError(
                "optimization_result must be an OptimizationResult."
            )


@dataclass(frozen=True, slots=True)
class WalkForwardResult:
    """
    Immutable complete walk-forward execution result.

    Attributes
    ----------
    iterations
        Chronological walk-forward iteration results.
    """

    iterations: tuple[
        WalkForwardIterationResult,
        ...]

    @property
    def iteration_count(self) -> int:
        """
        Return number of completed walk-forward iterations.
        """

        return len(
            self.iterations
        )

    @property
    def is_empty(self) -> bool:
        """
        Return True when no iterations exist.
        """

        return not self.iterations