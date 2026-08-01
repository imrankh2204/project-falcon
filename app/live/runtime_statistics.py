"""
Project Falcon

FAL-550-R2

Runtime Statistics

Immutable runtime execution statistics.

Responsibilities
----------------
- Represent runtime execution metrics.
- Remain immutable.
- Preserve broker independence.
- Provide deterministic runtime snapshots.

The model intentionally does NOT:

- Collect statistics.
- Process market events.
- Store orders.
- Calculate P&L.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass(frozen=True, slots=True)
class RuntimeStatistics:
    """
    Immutable snapshot of runtime execution statistics.
    """

    events_processed: int

    accepted_trades: int

    rejected_trades: int

    started_at: datetime | None = None

    finished_at: datetime | None = None

    elapsed: timedelta | None = None

    def __post_init__(self) -> None:
        """
        Validate runtime statistics.
        """

        for name, value in (
            ("events_processed", self.events_processed),
            ("accepted_trades", self.accepted_trades),
            ("rejected_trades", self.rejected_trades),
        ):
            if not isinstance(value, int):
                raise TypeError(
                    f"{name} must be an integer."
                )

            if value < 0:
                raise ValueError(
                    f"{name} cannot be negative."
                )

        if (
            self.started_at is not None
            and not isinstance(
                self.started_at,
                datetime,
            )
        ):
            raise TypeError(
                "started_at must be a datetime or None."
            )

        if (
            self.finished_at is not None
            and not isinstance(
                self.finished_at,
                datetime,
            )
        ):
            raise TypeError(
                "finished_at must be a datetime or None."
            )

        if (
            self.elapsed is not None
            and not isinstance(
                self.elapsed,
                timedelta,
            )
        ):
            raise TypeError(
                "elapsed must be a timedelta or None."
            )