"""
Immutable live event.

Represents an event flowing through Falcon's live market pipeline.

Responsibilities
----------------
- Wrap a normalized LiveTick.
- Provide an immutable transport object.
- Remain broker independent.

The model intentionally does NOT implement:

- Strategy logic
- Tick processing
- Indicator calculations
- Order execution
- Broker communication
"""

from __future__ import annotations

from dataclasses import dataclass

from app.live.live_tick import (
    LiveTick,
)


@dataclass(
    frozen=True,
    slots=True,
)
class LiveEvent:
    """
    Immutable live market event.
    """

    tick: LiveTick

    def __post_init__(
        self,
    ) -> None:
        """
        Validate the event.
        """

        if not isinstance(
            self.tick,
            LiveTick,
        ):
            raise TypeError(
                "tick must be a LiveTick."
            )