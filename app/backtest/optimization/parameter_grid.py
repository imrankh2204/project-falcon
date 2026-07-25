"""
Parameter grid generation for Project Falcon.

This module provides deterministic generation of EMA crossover parameter
combinations for strategy optimization.

Responsibilities
----------------
- Validate parameter ranges.
- Generate immutable EMACrossoverParameters.
- Skip invalid parameter combinations.
- Preserve deterministic iteration order.

The ParameterGrid intentionally does NOT implement:

- Strategy construction
- Backtest execution
- Result ranking
- Reporting
"""

from __future__ import annotations

from collections.abc import Iterable, Iterator

from app.strategies.ema_parameters import (
    EMACrossoverParameters,
)


class ParameterGrid:
    """
    Deterministic generator of EMA crossover parameter combinations.
    """

    def __init__(
        self,
        *,
        fast_periods: Iterable[int],
        slow_periods: Iterable[int],
    ) -> None:

        self._fast_periods = tuple(fast_periods)
        self._slow_periods = tuple(slow_periods)

        if not self._fast_periods:
            raise ValueError(
                "fast_periods cannot be empty."
            )

        if not self._slow_periods:
            raise ValueError(
                "slow_periods cannot be empty."
            )

        for value in (
            *self._fast_periods,
            *self._slow_periods,
        ):
            if not isinstance(value, int):
                raise TypeError(
                    "EMA periods must be integers."
                )

            if value <= 0:
                raise ValueError(
                    "EMA periods must be greater than zero."
                )

        self._parameters = tuple(
            EMACrossoverParameters(
                fast_period=fast,
                slow_period=slow,
            )
            for fast in self._fast_periods
            for slow in self._slow_periods
            if fast < slow
        )

    def __iter__(
        self,
    ) -> Iterator[EMACrossoverParameters]:
        """
        Iterate over valid parameter combinations.
        """

        return iter(self._parameters)

    def __len__(
        self,
    ) -> int:
        """
        Return number of valid parameter combinations.
        """

        return len(self._parameters)

    @property
    def parameters(
        self,
    ) -> tuple[EMACrossoverParameters, ...]:
        """
        Immutable parameter combinations.
        """

        return self._parameters