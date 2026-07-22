"""
Replay clock for Project Falcon.

Provides deterministic time progression during historical replay.

Responsibilities:
    - Maintain simulated replay time.
    - Advance time in chronological order.
    - Prevent backward time movement.

The ReplayClock intentionally does NOT implement:

    - Real system time
    - Scheduling
    - Sleeping
    - Replay orchestration
"""

from __future__ import annotations

from datetime import datetime


class ReplayClock:
    """
    Deterministic clock used by the replay engine.

    The clock advances only when instructed and never moves
    backwards.
    """

    def __init__(self, start_time: datetime) -> None:
        """
        Initialize the replay clock.

        Parameters
        ----------
        start_time:
            Initial simulated timestamp.
        """

        if not isinstance(start_time, datetime):
            raise TypeError(
                "start_time must be a datetime instance."
            )

        self._current_time = start_time

    @property
    def current_time(self) -> datetime:
        """
        Return the current simulated replay time.
        """
        return self._current_time

    def advance(self, new_time: datetime) -> None:
        """
        Advance the replay clock.

        Parameters
        ----------
        new_time:
            New simulated timestamp.

        Raises
        ------
        TypeError
            If new_time is not a datetime.

        ValueError
            If attempting to move the clock backwards.
        """

        if not isinstance(new_time, datetime):
            raise TypeError(
                "new_time must be a datetime instance."
            )

        if new_time < self._current_time:
            raise ValueError(
                "ReplayClock cannot move backwards."
            )

        self._current_time = new_time