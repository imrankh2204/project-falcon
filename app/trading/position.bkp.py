"""
Trading position domain model.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from app.market.instrument import Instrument
from app.strategies.signal import Signal
from app.trading.position_status import PositionStatus


@dataclass(slots=True)
class Position:
    """
    Represents an active or completed trading position.

    A Position is a lightweight domain entity that captures the
    state of a trade after successful execution.

    Responsibilities:
        - Hold position state.
        - Expose simple lifecycle properties.
    """

    position_id: str

    instrument: Instrument
    signal: Signal

    quantity: int

    entry_price: float
    entry_time: datetime

    status: PositionStatus = field(default=PositionStatus.OPEN)

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