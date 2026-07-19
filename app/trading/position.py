"""
Trading position domain model.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from app.market.instrument import Instrument
from app.strategies.signal import Signal
from app.trading.position_status import PositionStatus


class PositionLifecycleError(ValueError):
    """
    Raised when an invalid lifecycle transition is attempted.
    """


@dataclass(slots=True)
class Position:
    """
    Represents an active or completed trading position.

    A Position is the core trading domain entity responsible for
    maintaining its own lifecycle state.

    Responsibilities:
        - Hold immutable trade information.
        - Track lifecycle state.
        - Validate lifecycle transitions.
        - Record exit metadata.

    A Position intentionally does NOT perform:

        - P&L calculations
        - Brokerage calculations
        - Portfolio management
        - Execution logic
    """

    #
    # Identity
    #

    position_id: str

    #
    # Instrument & Strategy
    #

    instrument: Instrument
    signal: Signal

    #
    # Quantity
    #

    quantity: int

    #
    # Entry
    #

    entry_price: float
    entry_time: datetime

    #
    # Exit
    #

    exit_price: float | None = field(default=None)
    exit_time: datetime | None = field(default=None)

    #
    # Lifecycle
    #

    status: PositionStatus = field(
        default=PositionStatus.OPEN
    )

    @property
    def is_open(self) -> bool:
        """
        Return True when the position is currently open.
        """
        return self.status == PositionStatus.OPEN

    @property
    def is_closed(self) -> bool:
        """
        Return True when the position has been closed.
        """
        return self.status == PositionStatus.CLOSED

    def close(
        self,
        exit_price: float,
        exit_time: datetime,
    ) -> None:
        """
        Close the trading position.

        Parameters
        ----------
        exit_price:
            Executed exit price.

        exit_time:
            Timestamp of exit execution.

        Raises
        ------
        PositionLifecycleError
            If the lifecycle transition is invalid.
        """

        #
        # Validate lifecycle
        #

        if self.is_closed:
            raise PositionLifecycleError(
                "Position is already closed."
            )

        #
        # Validate exit price
        #

        if exit_price <= 0:
            raise PositionLifecycleError(
                "Exit price must be greater than zero."
            )
        
                #
        # Validate exit timestamp
        #

        if exit_time <= self.entry_time:
            raise PositionLifecycleError(
                "Exit time cannot be earlier than entry time."
            )

        #
        # Record exit information
        #

        self.exit_price = exit_price
        self.exit_time = exit_time

        #
        # Transition lifecycle
        #

        self.status = PositionStatus.CLOSED
        
        #
        # End of Position
        #