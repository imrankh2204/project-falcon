"""
Immutable walk-forward evaluation window.

This module defines the value object representing one
walk-forward optimization cycle.

Responsibilities
----------------
- Represent training period boundaries.
- Represent validation period boundaries.
- Provide immutable window information.

The WalkForwardWindow intentionally does NOT implement:

- Window generation
- Historical data loading
- Optimization execution
- Backtest execution
- Performance calculations
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class WalkForwardWindow:
    """
    Immutable walk-forward evaluation window.

    Attributes
    ----------
    training_start
        Beginning of the optimization training period.

    training_end
        End of the optimization training period.

    validation_start
        Beginning of the validation period.

    validation_end
        End of the validation period.
    """

    training_start: datetime

    training_end: datetime

    validation_start: datetime

    validation_end: datetime

    def __post_init__(self) -> None:
        """
        Validate window boundaries.
        """

        values = (
            (
                "training_start",
                self.training_start,
            ),
            (
                "training_end",
                self.training_end,
            ),
            (
                "validation_start",
                self.validation_start,
            ),
            (
                "validation_end",
                self.validation_end,
            ),
        )

        for name, value in values:

            if not isinstance(
                value,
                datetime,
            ):
                raise TypeError(
                    f"{name} must be a datetime."
                )

        if self.training_start >= self.training_end:
            raise ValueError(
                "training_start must be before training_end."
            )

        if self.validation_start >= self.validation_end:
            raise ValueError(
                "validation_start must be before validation_end."
            )

        if self.training_end > self.validation_start:
            raise ValueError(
                "Training period cannot overlap validation period."
            )

    @property
    def training_duration_days(self) -> int:
        """
        Return training period duration in days.
        """

        return (
            self.training_end
            -
            self.training_start
        ).days

    @property
    def validation_duration_days(self) -> int:
        """
        Return validation period duration in days.
        """

        return (
            self.validation_end
            -
            self.validation_start
        ).days