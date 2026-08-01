"""
Broker-independent live market data stream.

Defines the abstract interface for receiving live market data from a
broker.

Responsibilities
----------------
- Define stream lifecycle operations.
- Define subscription operations.
- Remain broker independent.

The interface intentionally does NOT define:

- Broker SDK callbacks
- Tick parsing
- Event dispatch
- Threading
- Authentication
- Reconnection
- Retry logic
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod


class MarketDataStream(ABC):
    """
    Broker-independent live market data stream.
    """

    @abstractmethod
    def connect(
        self,
    ) -> None:
        """
        Connect to the live market data stream.
        """

    @abstractmethod
    def disconnect(
        self,
    ) -> None:
        """
        Disconnect from the live market data stream.
        """

    @abstractmethod
    def subscribe(
        self,
        instrument_tokens: tuple[
            int,
            ...,
        ],
    ) -> None:
        """
        Subscribe to live market data.

        Parameters
        ----------
        instrument_tokens
            Broker instrument tokens.
        """

    @abstractmethod
    def unsubscribe(
        self,
        instrument_tokens: tuple[
            int,
            ...,
        ],
    ) -> None:
        """
        Unsubscribe from live market data.

        Parameters
        ----------
        instrument_tokens
            Broker instrument tokens.
        """