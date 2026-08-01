"""
Concrete Zerodha authentication implementation.

Bootstraps an authenticated Kite Connect client from the Falcon
configuration.

Responsibilities
----------------
- Create an authenticated KiteConnect client.
- Produce immutable AuthenticationResult objects.
- Hide Kite SDK initialization details.

This implementation intentionally does NOT perform the interactive
OAuth login flow. It assumes a valid access token is already available.
"""

from __future__ import annotations

from datetime import datetime

from kiteconnect import KiteConnect
from kiteconnect import KiteTicker

from app.broker.zerodha.authentication import (
    ZerodhaAuthentication,
)
from app.broker.zerodha.authentication_result import (
    AuthenticationResult,
)
from app.broker.zerodha.zerodha_session import (
    ZerodhaSession,
)
from app.config.loader import load_configuration


class KiteAuthentication(
    ZerodhaAuthentication,
):
    """
    Bootstrap authentication using a configured access token.
    """

    def authenticate(
        self,
    ) -> AuthenticationResult:
        """
        Authenticate using the configured Kite access token.
        """

        config = load_configuration()

        broker = config["broker"]

        api_key = broker["kite_api_key"]
        access_token = broker["kite_access_token"]

        if not api_key:
            raise ValueError(
                "KITE_API_KEY is not configured."
            )

        if not access_token:
            raise ValueError(
                "KITE_ACCESS_TOKEN is not configured."
            )

        kite = KiteConnect(
            api_key=api_key,
        )

        kite.set_access_token(
            access_token,
        )

        kite_ticker = KiteTicker(
            api_key=api_key,
            access_token=access_token,
        )

        profile = kite.profile()

        now = datetime.now()

        session = ZerodhaSession(
            broker_name="zerodha",
            access_token=access_token,
            public_token="bootstrap",
            user_id=profile["user_id"],
            login_time=now,
            authenticated_at=now,
            expires_at=None,
        )

        return AuthenticationResult(
            session=session,
            kite=kite,
            kite_ticker=kite_ticker,
        )