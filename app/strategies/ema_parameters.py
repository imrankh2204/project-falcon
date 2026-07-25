"""
Immutable EMA crossover strategy parameters for Project Falcon.

This module defines the immutable configuration object used to
construct EMACrossoverStrategy instances.

Responsibilities
----------------
- Hold validated strategy parameters.
- Enforce parameter invariants.
- Remain immutable.

The parameter model intentionally does NOT implement:

- Strategy logic
- Indicator calculations
- Factory logic
- Replay functionality
- Trading functionality
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class EMACrossoverParameters:
    """
    Immutable configuration for EMA crossover strategy.

    Parameters
    ----------
    fast_period
        Period for the fast EMA.

    slow_period
        Period for the slow EMA.
    """

    fast_period: int
    slow_period: int

    def __post_init__(self) -> None:
        """
        Validate parameter values.

        Raises
        ------
        TypeError
            If either parameter is not an integer.

        ValueError
            If either period is non-positive or the fast period is
            greater than or equal to the slow period.
        """

        if not isinstance(self.fast_period, int):
            raise TypeError(
                "fast_period must be an integer."
            )

        if not isinstance(self.slow_period, int):
            raise TypeError(
                "slow_period must be an integer."
            )

        if self.fast_period <= 0:
            raise ValueError(
                "fast_period must be greater than zero."
            )

        if self.slow_period <= 0:
            raise ValueError(
                "slow_period must be greater than zero."
            )

        if self.fast_period >= self.slow_period:
            raise ValueError(
                "fast_period must be less than slow_period."
            )