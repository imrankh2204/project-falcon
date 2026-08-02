from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class BrokerConfig:
    """
    Immutable broker configuration.

    Stores broker-independent configuration required to establish
    a broker connection.
    """

    broker_name: str

    api_key: str

    api_secret: str | None = None

    redirect_url: str | None = None

    sandbox: bool = False

    def __post_init__(self) -> None:

        if not isinstance(self.broker_name, str):
            raise TypeError(
                "broker_name must be a string."
            )

        if not self.broker_name.strip():
            raise ValueError(
                "broker_name cannot be empty."
            )

        if not isinstance(self.api_key, str):
            raise TypeError(
                "api_key must be a string."
            )

        if not self.api_key.strip():
            raise ValueError(
                "api_key cannot be empty."
            )

        if (
            self.api_secret is not None
            and not isinstance(
                self.api_secret,
                str,
            )
        ):
            raise TypeError(
                "api_secret must be a string or None."
            )

        if (
            self.redirect_url is not None
            and not isinstance(
                self.redirect_url,
                str,
            )
        ):
            raise TypeError(
                "redirect_url must be a string or None."
            )