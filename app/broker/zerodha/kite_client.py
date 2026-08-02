"""
Kite Connect client wrapper for Project Falcon.

Encapsulates the official Kite Connect SDK behind a thin adapter.

Responsibilities
----------------
- Construct the Kite SDK client.
- Own the SDK instance.
- Expose only Falcon-approved operations.
- Prevent SDK leakage into the Falcon domain.

The wrapper intentionally does NOT implement:

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

    def login_url(
        self,
    ) -> str:
        """
        Return the Zerodha login URL.
        """

        return self._client.login_url()

    def generate_session(
        self,
        request_token: str,
    ) -> dict:
        """
        Exchange a request token for a broker session.
        """

        if not isinstance(
            request_token,
            str,
        ):
            raise TypeError(
                "request_token must be a string."
            )

        if not request_token.strip():
            raise ValueError(
                "request_token cannot be empty."
            )

        if self._config.api_secret is None:
            raise ValueError(
                "Broker configuration does not contain an API secret."
            )

        return self._client.generate_session(
            request_token=request_token,
            api_secret=self._config.api_secret,
        )

    def set_access_token(
        self,
        access_token: str,
    ) -> None:
        """
        Configure the SDK with an access token.
        """

        if not isinstance(
            access_token,
            str,
        ):
            raise TypeError(
                "access_token must be a string."
            )

        if not access_token.strip():
            raise ValueError(
                "access_token cannot be empty."
            )

        self._client.set_access_token(
            access_token,
        )