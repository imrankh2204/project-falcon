"""
Immutable broker session model for Project Falcon.

Represents an authenticated broker session.

Responsibilities
----------------
- Store immutable authentication state.
- Remain broker independent.
- Provide deterministic transport semantics.

The model intentionally does NOT implement:

- Authentication
- Token refresh
- Session persistence
- Broker communication
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from app.live.session_status import SessionStatus

@dataclass(frozen=True, slots=True)
class BrokerSession:
    """
    Immutable authenticated broker session.
    """

    broker_name: str

    user_id: str

    access_token: str

    authenticated_at: datetime

    expires_at: datetime | None = None

    status: SessionStatus = SessionStatus.AUTHENTICATED

    def __post_init__(self) -> None:
        """
        Validate the broker session.
        """

        if not isinstance(
            self.broker_name,
            str,
        ):
            raise TypeError(
                "broker_name must be a string."
            )

        if not self.broker_name.strip():
            raise ValueError(
                "broker_name cannot be empty."
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
            self.authenticated_at,
            datetime,
        ):
            raise TypeError(
                "authenticated_at must be a datetime."
            )

        if (
            self.expires_at is not None
            and not isinstance(
                self.expires_at,
                datetime,
            )
        ):
            raise TypeError(
                "expires_at must be a datetime or None."
            )
        if not isinstance(
            self.status,
            SessionStatus,
        ):
            raise TypeError(
                "status must be a SessionStatus."
            )

    @property
    def has_expiry(self) -> bool:
        """
        Return True if the session expires.
        """

        return self.expires_at is not None

    @property
    def is_expired(self) -> bool:
        """
        Return True if the session has expired.
        """

        if self.expires_at is None:
            return False

        return datetime.now(
            tz=self.expires_at.tzinfo
        ) >= self.expires_at