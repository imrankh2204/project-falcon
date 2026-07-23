"""
Replay event domain model for Project Falcon.

Represents one deterministic event emitted during historical replay.

Responsibilities:
    - Carry replay timestamp.
    - Carry the associated market candle.

The ReplayEvent intentionally does NOT implement:

    - Replay progression
    - Data loading
    - Strategy execution
    - Order execution
    - Portfolio updates
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from app.market.candle import Candle


@dataclass(frozen=True, slots=True)
class ReplayEvent:
    """
    Immutable historical replay event.

    A ReplayEvent represents one point in simulated market time
    and contains the candle associated with that replay moment.

    Attributes
    ----------
    timestamp:
        Simulated replay timestamp.

    candle:
        Market candle associated with this event.
    """

    timestamp: datetime
    candle: Candle