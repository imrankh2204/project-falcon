"""
Authentication service for Zerodha Kite Connect.

Responsible for exchanging a request token for an authenticated
Falcon BrokerSession.

The service intentionally hides all Kite SDK response details from
the rest of the application.
"""

from __future__ import annotations

from datetime import datetime

from app.live.broker_session import BrokerSession
from app.live.exceptions import AuthenticationError

from .kite_client import KiteClient


class AuthenticationService:
    """
    Performs authentication using the Kite client.
    """

    def __init__(
        self,
        client: KiteClient,
    ) -> None:

        if not isinstance(
            client,
            KiteClient,
        ):
            raise TypeError(
                "client must be a KiteClient."
            )

        self._client = client

    def authenticate(
        self,
        request_token: str,
        api_secret: str,
    ) -> BrokerSession:
        """
        Exchange a request token for an authenticated BrokerSession.
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

        if not isinstance(
            api_secret,
            str,
        ):
            raise TypeError(
                "api_secret must be a string."
            )

        if not api_secret.strip():
            raise ValueError(
                "api_secret cannot be empty."
            )

        try:

            session_data = (
                self._client.generate_session(
                    request_token=request_token,
                    api_secret=api_secret,
                )
            )

        except Exception as exc:

            raise AuthenticationError(
                "Authentication with broker failed."
            ) from exc

        if not isinstance(
            session_data,
            dict,
        ):
            raise AuthenticationError(
                "Broker returned an invalid session response."
            )

        access_token = session_data.get(
            "access_token"
        )

        user_id = session_data.get(
            "user_id"
        )

        if (
            not isinstance(
                access_token,
                str,
            )
            or not access_token.strip()
        ):
            raise AuthenticationError(
                "Broker session is missing a valid access token."
            )

        if (
            not isinstance(
                user_id,
                str,
            )
            or not user_id.strip()
        ):
            raise AuthenticationError(
                "Broker session is missing a valid user id."
            )

        self._client.set_access_token(
            access_token
        )

        return BrokerSession(
            broker_name=self._client.broker_name,
            user_id=user_id,
            access_token=access_token,
            authenticated_at=datetime.now(),
        )