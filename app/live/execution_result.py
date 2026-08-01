"""
Immutable execution result model for Project Falcon.

Represents the broker acknowledgement returned after an order
submission.

Responsibilities
----------------
- Store immutable execution outcome.
- Remain broker independent.
- Encapsulate broker acknowledgement.
- Provide deterministic transport semantics.

The model intentionally does NOT implement:

- Order placement
- Broker communication
- Retry logic
- Order polling
"""

from __future__ import annotations

from dataclasses import dataclass

from app.live.order import Order


@dataclass(frozen=True, slots=True)
class ExecutionResult:
    """
    Immutable broker execution result.
    """

    order: Order

    accepted: bool

    message: str | None = None

    def __post_init__(self) -> None:
        """
        Validate the execution result.
        """

        if not isinstance(
            self.order,
            Order,
        ):
            raise TypeError(
                "order must be an Order."
            )

        if not isinstance(
            self.accepted,
            bool,
        ):
            raise TypeError(
                "accepted must be a bool."
            )

        if (
            self.message is not None
            and not isinstance(
                self.message,
                str,
            )
        ):
            raise TypeError(
                "message must be a string or None."
            )

        if (
            isinstance(
                self.message,
                str,
            )
            and not self.message.strip()
        ):
            raise ValueError(
                "message cannot be empty."
            )