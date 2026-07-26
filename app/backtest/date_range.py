"""
Immutable date range model for Project Falcon.

Defines execution boundaries used by backtesting and walk-forward
validation.

Responsibilities
----------------
- Store start and end timestamps.
- Validate chronological ordering.
- Provide immutable access to boundaries.

The DateRange intentionally does NOT implement:

- Candle loading
- Dataset filtering
- Backtest execution
- Reporting
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class DateRange:
    """
    Immutable execution date range.

    Parameters
    ----------
    start_time
        Inclusive range start timestamp.

    end_time
        Inclusive range end timestamp.
    """

    start_time: datetime
    end_time: datetime

    def __post_init__(self) -> None:
        """
        Validate date range boundaries.

        Raises
        ------
        TypeError
            If timestamps are invalid.

        ValueError
            If end_time precedes start_time.
        """

        if not isinstance(
            self.start_time,
            datetime,
        ):
            raise TypeError(
                "start_time must be a datetime."
            )

        if not isinstance(
            self.end_time,
            datetime,
        ):
            raise TypeError(
                "end_time must be a datetime."
            )

        if self.end_time < self.start_time:
            raise ValueError(
                "end_time must be greater than or equal to start_time."
            )