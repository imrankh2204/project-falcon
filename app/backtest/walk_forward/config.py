"""
Immutable walk-forward optimization configuration.

This module defines the configuration object used to control
walk-forward evaluation.

Responsibilities
----------------
- Hold training window size.
- Hold validation window size.
- Hold rolling step size.
- Validate configuration values.

The WalkForwardConfig intentionally does NOT implement:

- Window generation
- Optimization execution
- Backtest execution
- Result aggregation
- Reporting
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class WalkForwardConfig:
    """
    Immutable walk-forward optimization configuration.

    Parameters
    ----------
    training_days
        Number of historical days used for optimization.

    validation_days
        Number of future days used for out-of-sample validation.

    step_days
        Number of days the window advances after each iteration.
    """

    training_days: int

    validation_days: int

    step_days: int

    def __post_init__(self) -> None:
        """
        Validate configuration values.

        Raises
        ------
        TypeError
            If values are not integers.

        ValueError
            If values are not greater than zero.
        """

        for name, value in (
            (
                "training_days",
                self.training_days,
            ),
            (
                "validation_days",
                self.validation_days,
            ),
            (
                "step_days",
                self.step_days,
            ),
        ):

            if not isinstance(
                value,
                int,
            ):
                raise TypeError(
                    f"{name} must be an integer."
                )

            if value <= 0:
                raise ValueError(
                    f"{name} must be greater than zero."
                )