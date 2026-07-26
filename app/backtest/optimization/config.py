"""
Immutable optimization configuration for Project Falcon.

This module defines the immutable configuration object used to
control optimization execution.

Responsibilities
----------------
- Hold optimization search space.
- Hold ranking configuration.
- Hold optional optimization date range.
- Validate configuration values.

The OptimizationConfig intentionally does NOT implement:

- Parameter generation
- Strategy construction
- Backtest execution
- Ranking
- Report generation
"""

from __future__ import annotations

from dataclasses import dataclass

from app.backtest.date_range import DateRange
from app.backtest.optimization.ranking import (
    RankingMetric,
)


@dataclass(frozen=True, slots=True)
class OptimizationConfig:
    """
    Immutable optimization configuration.
    """

    fast_periods: tuple[int, ...]
    slow_periods: tuple[int, ...]

    ranking_metric: RankingMetric

    max_combinations: int | None = None

    date_range: DateRange | None = None

    def __post_init__(self) -> None:

        if not self.fast_periods:
            raise ValueError(
                "fast_periods cannot be empty."
            )

        if not self.slow_periods:
            raise ValueError(
                "slow_periods cannot be empty."
            )

        if not isinstance(
            self.ranking_metric,
            RankingMetric,
        ):
            raise TypeError(
                "ranking_metric must be a RankingMetric."
            )

        for period in (
            *self.fast_periods,
            *self.slow_periods,
        ):

            if not isinstance(period, int):
                raise TypeError(
                    "EMA periods must be integers."
                )

            if period <= 0:
                raise ValueError(
                    "EMA periods must be greater than zero."
                )

        if (
            self.max_combinations
            is not None
        ):

            if not isinstance(
                self.max_combinations,
                int,
            ):
                raise TypeError(
                    "max_combinations must be an integer or None."
                )

            if self.max_combinations <= 0:
                raise ValueError(
                    "max_combinations must be greater than zero."
                )

        if (
            self.date_range
            is not None
            and not isinstance(
                self.date_range,
                DateRange,
            )
        ):
            raise TypeError(
                "date_range must be a DateRange or None."
            )