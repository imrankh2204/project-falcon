"""
Kite Connect client wrapper for Project Falcon.

Encapsulates the official Kite Connect SDK behind a thin adapter.

Responsibilities
----------------
- Construct the Kite SDK client.
- Own the SDK instance.
- Prevent SDK leakage into the Falcon domain.

The wrapper intentionally does NOT implement:

- Authentication
- Session creation
- Order placement
- Market data
- WebSocket handling
"""

from __future__ import annotations

from kiteconnect import KiteConnect

from app.broker.broker_config import BrokerConfig


class KiteClient:
    """
    Thin wrapper around the Kite Connect SDK.
    """

    def __init__(
        self,
        config: BrokerConfig,
    ) -> None:
        """
        Construct a Kite SDK client.
        """

        if not isinstance(
            config,
            BrokerConfig,
        ):
            raise TypeError(
                "config must be a BrokerConfig."
            )

        self._config = config

        self._client = KiteConnect(
            api_key=config.api_key,
        )

    @property
    def broker_name(
        self,
    ) -> str:
        """
        Return the configured broker name.
        """

        return self._config.broker_name

    @property
    def client(
        self,
    ) -> KiteConnect:
        """
        Return the encapsulated SDK client.

        This property is intended for broker-layer
        implementations only.
        """

        return self._client