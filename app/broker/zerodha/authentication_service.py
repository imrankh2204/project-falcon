"""
Kite authentication service for Project Falcon.

Exchanges a Kite request token for an authenticated Falcon
BrokerSession while keeping all Kite SDK response handling
inside the broker layer.

Responsibilities
----------------
- Perform session exchange.
- Translate SDK response into BrokerSession.
- Prevent SDK response leakage into the domain.

The service intentionally does NOT implement:

- Browser login
- Redirect handling
- Token persistence
- Session refresh
- Re-authentication
"""

from __future__ import annotations

from datetime import datetime

from app.broker.broker_config import BrokerConfig
from app.broker.zerodha.kite_client import KiteClient
from app.live.broker_session import BrokerSession
from app.live.session_status import SessionStatus


class AuthenticationService:
    """
    Broker-layer authentication service.
    """

    def __init__(
        self,
        config: BrokerConfig,
        client: KiteClient,
    ) -> None:

        if not isinstance(config, BrokerConfig):
            raise TypeError(
                "config must be a BrokerConfig."
            )

        if not isinstance(client, KiteClient):
            raise TypeError(
                "client must be a KiteClient."
            )

        self._config = config
        self._client = client

    def authenticate(
        self,
        request_token: str,
    ) -> BrokerSession:
        """
        Exchange a request token for a BrokerSession.
        """

        if not isinstance(request_token, str):
            raise TypeError(
                "request_token must be a string."
            )

        if not request_token.strip():
            raise ValueError(
                "request_token cannot be empty."
            )

        session_data = self._client.generate_session(
            request_token
        )

        access_token = session_data["access_token"]
        user_id = session_data["user_id"]

        self._client.set_access_token(
            access_token
        )

        return BrokerSession(
            broker_name=self._config.broker_name,
            user_id=user_id,
            access_token=access_token,
            authenticated_at=datetime.now(),
            expires_at=None,
            status=SessionStatus.AUTHENTICATED,
        )