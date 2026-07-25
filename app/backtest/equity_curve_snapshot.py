"""
Immutable equity curve analytics snapshot for Project Falcon.

This module defines immutable value objects representing the
calculated equity curve produced by the analytics layer.

Responsibilities
----------------
- Represent chronological equity observations.
- Represent aggregate drawdown statistics.
- Provide immutable transport objects.

The models intentionally contain no business logic and are created
exclusively by EquityCurve.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class EquityPoint:
    """
    Single observation on the equity curve.

    Attributes
    ----------
    timestamp
        Time at which the equity value was recorded.

    equity
        Account equity after the corresponding trade closed.
    """

    timestamp: datetime
    equity: float


@dataclass(frozen=True, slots=True)
class EquityCurveSnapshot:
    """
    Immutable equity curve analysis.

    Attributes
    ----------
    points
        Chronological equity observations.

    peak_equity
        Highest account equity reached.

    maximum_drawdown
        Largest absolute decline from the historical peak.

    maximum_drawdown_percentage
        Largest drawdown expressed as a percentage of the
        corresponding peak equity.
    """

    points: tuple[EquityPoint, ...]

    peak_equity: float

    maximum_drawdown: float

    maximum_drawdown_percentage: float

    @property
    def final_equity(self) -> float:
        """
        Return the final recorded equity.

        Returns
        -------
        float
            Final account equity. Returns the peak equity when no
            observations exist (representing the initial capital).
        """

        if self.points:
            return self.points[-1].equity

        return self.peak_equity

    @property
    def observation_count(self) -> int:
        """
        Return the number of recorded equity observations.
        """

        return len(self.points)

    @property
    def is_empty(self) -> bool:
        """
        Return True when no equity observations exist.
        """

        return not self.points