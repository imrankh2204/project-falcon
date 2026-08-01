"""
Project Falcon

FAL-600-R1

Market Feed Contract

Defines the broker-independent abstraction for all market event
providers.

Responsibilities
----------------
- Define the lifecycle of a market feed.
- Provide deterministic event iteration.
- Remain broker independent.

The contract intentionally does NOT implement:

- Replay logic
- Broker connectivity
- WebSocket handling
- Historical loading
"""

from __future__ import annotations

from typing import Any, Iterable, Protocol


class MarketFeed(Protocol):
    """
    Broker-independent market feed contract.

    Implementations may source events from:

    - ReplayEngine
    - Broker WebSocket
    - Historical files
    - Simulators

    The runtime depends only on this interface.
    """

    def start(self) -> None:
        """
        Start the market feed.
        """
        ...

    def stop(self) -> None:
        """
        Stop the market feed.
        """
        ...

    def events(self) -> Iterable[Any]:
        """
        Produce market events in deterministic order.

        Returns
        -------
        Iterable[Any]
            Stream of market events.
        """
        ...