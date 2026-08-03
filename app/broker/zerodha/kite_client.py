"""
Kite Connect client wrapper for Project Falcon.

Encapsulates the official Kite Connect SDK behind a thin adapter.
"""

from __future__ import annotations

from kiteconnect import KiteConnect

from app.broker.broker_config import BrokerConfig
from app.broker.exceptions import BrokerAuthenticationError


class KiteClient:
    """
    Thin wrapper around the Kite Connect SDK.
    """

    def __init__(
        self,
        config: BrokerConfig,
    ) -> None:

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
        return self._config.broker_name

    def login_url(
        self,
    ) -> str:
        return self._client.login_url()

    def generate_session(
        self,
        request_token: str,
        api_secret: str,
    ) -> dict:

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

        return self._client.generate_session(
            request_token=request_token,
            api_secret=api_secret,
        )

    def set_access_token(
        self,
        access_token: str,
    ) -> None:

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

    def get_profile(
        self,
    ) -> dict:

        try:
            profile = self._client.profile()

        except Exception as exc:

            raise BrokerAuthenticationError(
                "Unable to retrieve broker profile."
            ) from exc

        if not isinstance(
            profile,
            dict,
        ):
            raise BrokerAuthenticationError(
                "Broker returned an invalid profile."
            )

        return profile

    def get_margins(self) -> dict:
        """
        Retrieve the current broker margin payload.
        """

        try:
            margins = self._client.margins()

        except Exception as exc:
            raise BrokerAuthenticationError(
                "Unable to retrieve broker margins."
            ) from exc

        if not isinstance(
            margins,
            dict,
        ):
            raise BrokerAuthenticationError(
                "Broker returned an invalid margin payload."
            )

        return margins