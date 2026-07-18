"""
Paper broker implementation for Project Falcon.

Implements the BrokerClient interface without connecting
to an external broker.
"""

from __future__ import annotations

from app.broker.broker_client import BrokerClient
from app.core.logger import get_logger


class PaperBroker(BrokerClient):
    """
    Simple paper broker implementation.
    """

    def __init__(self) -> None:
        self.logger = get_logger("paper_broker")
        self._connected = False

    def connect(self) -> None:
        self.logger.info("Connecting paper broker...")
        self._connected = True

    def disconnect(self) -> None:
        self.logger.info("Disconnecting paper broker...")
        self._connected = False

    def is_connected(self) -> bool:
        return self._connected

    def download_instruments(self) -> None:
        self.logger.info(
            "Paper broker does not require instrument download."
        )

    def get_ltp(self, symbol: str) -> float:
        raise NotImplementedError(
            "PaperBroker.get_ltp() is not implemented yet."
        )

    def place_order(self, **kwargs) -> str:
        raise NotImplementedError(
            "PaperBroker.place_order() is not implemented yet."
        )

    def cancel_order(self, order_id: str) -> bool:
        raise NotImplementedError(
            "PaperBroker.cancel_order() is not implemented yet."
        )

    def get_positions(self):
        return []

    def get_orders(self):
        return []