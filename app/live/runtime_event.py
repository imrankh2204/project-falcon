"""
Project Falcon

FAL-560-R1

Runtime Event

Immutable runtime event model.

Responsibilities
----------------
- Represent a processed runtime event.
- Preserve deterministic event ordering.
- Remain broker independent.
- Support runtime diagnostics.

The model intentionally does NOT implement:

- Event processing.
- Trade execution.
- Strategy evaluation.
- Logging.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class RuntimeEvent:
    """
    Immutable runtime event snapshot.
    """

    sequence: int

    timestamp: datetime

    accepted: bool

    description: str

    def __post_init__(self) -> None:

        if not isinstance(self.sequence, int):
            raise TypeError(
                "sequence must be an integer."
            )

        if self.sequence < 1:
            raise ValueError(
                "sequence must be greater than zero."
            )

        if not isinstance(
            self.timestamp,
            datetime,
        ):
            raise TypeError(
                "timestamp must be a datetime."
            )

        if not isinstance(
            self.accepted,
            bool,
        ):
            raise TypeError(
                "accepted must be a bool."
            )

        if not isinstance(
            self.description,
            str,
        ):
            raise TypeError(
                "description must be a string."
            )

        if not self.description.strip():
            raise ValueError(
                "description cannot be empty."
            )