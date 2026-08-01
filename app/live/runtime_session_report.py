"""
Project Falcon

FAL-570-R1

Runtime Session Report

Immutable aggregate representing a completed runtime session.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.live.runtime_event import RuntimeEvent
from app.live.runtime_statistics import RuntimeStatistics


@dataclass(frozen=True, slots=True)
class RuntimeSessionReport:
    """
    Immutable runtime session report.

    Aggregates runtime statistics together with the
    chronological runtime event history.
    """

    statistics: RuntimeStatistics

    events: tuple[RuntimeEvent, ...]

    def __post_init__(self) -> None:
        """
        Validate the report.
        """

        if not isinstance(
            self.statistics,
            RuntimeStatistics,
        ):
            raise TypeError(
                "statistics must be a RuntimeStatistics."
            )

        if not isinstance(
            self.events,
            tuple,
        ):
            raise TypeError(
                "events must be a tuple."
            )

        for event in self.events:

            if not isinstance(
                event,
                RuntimeEvent,
            ):
                raise TypeError(
                    "events must contain RuntimeEvent instances."
                )