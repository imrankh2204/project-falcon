"""
Broker interface for Project Falcon.

Defines the abstract contract that every broker
implementation must satisfy.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class BrokerClient(ABC):
    """
    Abstract broker interface.
    """

    @abstractmethod
    def connect(self) -> None:
        """Establish broker connection."""

    @abstractmethod
    def disconnect(self) -> None:
        """Close broker connection."""

    @abstractmethod
    def is_connected(self) -> bool:
        """Return connection status."""

    @abstractmethod
    def download_instruments(self) -> None:
        """Download and cache instrument master."""

    @abstractmethod
    def get_ltp(self, symbol: str) -> float:
        """Return latest traded price."""

    @abstractmethod
    def place_order(self, **kwargs) -> str:
        """Place an order."""

    @abstractmethod
    def cancel_order(self, order_id: str) -> bool:
        """Cancel an order."""

    @abstractmethod
    def get_positions(self):
        """Return current positions."""

    @abstractmethod
    def get_orders(self):
        """Return order book."""