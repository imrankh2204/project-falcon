"""
Immutable live market tick.

Represents a normalized market tick independent of any broker SDK.

Responsibilities
----------------
- Store immutable market data.
- Remain broker independent.
- Provide deterministic transport semantics.

The model intentionally does NOT implement:

- Tick processing
- Indicator calculations
- Strategy logic
- Order execution
- Broker communication
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(
    frozen=True,
    slots=True,
)
class LiveTick:
    """
    Immutable normalized market tick.
    """

    instrument_token: int

    last_price: float

    volume: int

    open_interest: int

    timestamp: datetime

    def __post_init__(
        self,
    ) -> None:
        """
        Validate the tick.
        """

        if not isinstance(
            self.instrument_token,
            int,
        ):
            raise TypeError(
                "instrument_token must be an int."
            )

        if self.instrument_token <= 0:
            raise ValueError(
                "instrument_token must be positive."
            )

        if not isinstance(
            self.last_price,
            (int, float),
        ):
            raise TypeError(
                "last_price must be numeric."
            )

        if self.last_price <= 0:
            raise ValueError(
                "last_price must be positive."
            )

        if not isinstance(
            self.volume,
            int,
        ):
            raise TypeError(
                "volume must be an int."
            )

        if self.volume < 0:
            raise ValueError(
                "volume cannot be negative."
            )

        if not isinstance(
            self.open_interest,
            int,
        ):
            raise TypeError(
                "open_interest must be an int."
            )

        if self.open_interest < 0:
            raise ValueError(
                "open_interest cannot be negative."
            )

        if not isinstance(
            self.timestamp,
            datetime,
        ):
            raise TypeError(
                "timestamp must be a datetime."
            )