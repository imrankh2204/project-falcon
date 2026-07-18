"""
Zerodha broker implementation for Project Falcon.

Skeleton implementation of BrokerClient.
Actual Kite Connect integration will be added
in subsequent releases.
"""

from __future__ import annotations

from app.broker.broker_client import BrokerClient
from app.core.logger import get_logger
from kiteconnect import KiteConnect
from app.config.manager import get_config


class ZerodhaBroker(BrokerClient):
    """
    Zerodha broker implementation.
    """

    def __init__(self) -> None:
        self.logger = get_logger("zerodha_broker")
        self._connected = False

        config = get_config()

        self._api_key = config.broker.kite_api_key
        self._api_secret = config.broker.kite_api_secret
        self._access_token = config.broker.kite_access_token

        self.kite = KiteConnect(api_key=self._api_key)

    def connect(self) -> None:
        raise NotImplementedError(
            "Zerodha connection not implemented yet."
        )

    def disconnect(self) -> None:
        self._connected = False

    def is_connected(self) -> bool:
        return self._connected

    def download_instruments(self) -> None:
        raise NotImplementedError(
            "Instrument download not implemented yet."
        )

    def get_ltp(self, symbol: str) -> float:
        raise NotImplementedError(
            "LTP retrieval not implemented yet."
        )

    def place_order(self, **kwargs) -> str:
        raise NotImplementedError(
            "Order placement not implemented yet."
        )

    def cancel_order(self, order_id: str) -> bool:
        raise NotImplementedError(
            "Order cancellation not implemented yet."
        )

    def get_positions(self):
        raise NotImplementedError(
            "Position retrieval not implemented yet."
        )

    def get_orders(self):
        raise NotImplementedError(
            "Order retrieval not implemented yet."
        )