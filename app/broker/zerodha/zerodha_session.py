"""
Immutable Zerodha broker session for Project Falcon.

This module provides the concrete implementation of the broker session
contract for the Zerodha Kite Connect integration.

Responsibilities
----------------
- Represent an authenticated Zerodha session.
- Store immutable authentication metadata.
- Remain independent from authentication workflow.

The session intentionally does NOT implement:

- Authentication
- Token refresh
- Token persistence
- Order execution
- Quote retrieval
- Position management
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from app.live.broker_session import BrokerSession


@dataclass(frozen=True, slots=True)
class ZerodhaSession(BrokerSession):
    """
    Immutable authenticated Zerodha session.

    Parameters
    ----------
    access_token
        Kite Connect access token.

    public_token
        Public session token supplied by the broker.

    user_id
        Zerodha client identifier.

    login_time
        Timestamp when the session was established.
    """

    access_token: str

    public_token: str

    user_id: str

    login_time: datetime

    def __post_init__(self) -> None:
        """
        Validate session contents.
        """

        if not isinstance(
            self.access_token,
            str,
        ):
            raise TypeError(
                "access_token must be a string."
            )

        if not self.access_token.strip():
            raise ValueError(
                "access_token cannot be empty."
            )

        if not isinstance(
            self.public_token,
            str,
        ):
            raise TypeError(
                "public_token must be a string."
            )

        if not self.public_token.strip():
            raise ValueError(
                "public_token cannot be empty."
            )

        if not isinstance(
            self.user_id,
            str,
        ):
            raise TypeError(
                "user_id must be a string."
            )

        if not self.user_id.strip():
            raise ValueError(
                "user_id cannot be empty."
            )

        if not isinstance(
            self.login_time,
            datetime,
        ):
            raise TypeError(
                "login_time must be a datetime."
            )

    @property
    def authenticated(self) -> bool:
        """
        Return True when the session contains a valid access token.
        """

        return bool(self.access_token)

    def __repr__(self) -> str:
        """
        Safe representation that never exposes tokens.
        """

        return (
            f"{self.__class__.__name__}("
            f"user_id={self.user_id!r}, "
            f"login_time={self.login_time.isoformat()})"
        )