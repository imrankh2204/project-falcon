"""
Broker factory for Project Falcon.

Creates broker implementations based on the configured
broker type.
"""

from __future__ import annotations

from app.broker.broker_client import BrokerClient
from app.broker.paper_broker import PaperBroker
from app.config.manager import get_config


class BrokerFactory:
    """
    Creates broker instances.
    """

    @staticmethod
    def create() -> BrokerClient:

        config = get_config()

        broker = config.broker.broker.lower()

        if broker == "paper":
            return PaperBroker()

        if broker == "zerodha":
            raise NotImplementedError(
                "ZerodhaBroker is not implemented yet."
            )

        raise ValueError(
            f"Unsupported broker: {broker}"
        )