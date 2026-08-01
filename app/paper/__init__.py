"""
Paper trading implementation for Project Falcon.

This package contains the in-memory broker implementation used for
paper trading. It implements the BrokerGateway contract without any
external broker SDKs or network communication.

Responsibilities
----------------
- Provide deterministic paper order execution.
- Maintain in-memory broker state.
- Simulate broker authentication.
- Remain fully broker independent.

The package intentionally does NOT implement:

- Real broker connectivity
- Network communication
- Persistent storage
- Strategy execution
"""

from app.paper.paper_broker_gateway import (
    PaperBrokerGateway,
)

__all__ = [
    "PaperBrokerGateway",
]