"""
Immutable broker profile domain model for Project Falcon.

Represents broker-neutral profile details retrieved from a broker.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class BrokerProfile:
    """
    Immutable broker profile payload.
    """

    broker_name: str
    user_id: str
    user_name: str | None = None
    email: str | None = None
    mobile: str | None = None

    def __post_init__(self) -> None:
        """
        Validate the profile fields.
        """

        if not isinstance(self.broker_name, str):
            raise TypeError("broker_name must be a string.")

        if not self.broker_name.strip():
            raise ValueError("broker_name cannot be empty.")

        if not isinstance(self.user_id, str):
            raise TypeError("user_id must be a string.")

        if not self.user_id.strip():
            raise ValueError("user_id cannot be empty.")

        if self.user_name is not None and not isinstance(self.user_name, str):
            raise TypeError("user_name must be a string or None.")

        if self.email is not None and not isinstance(self.email, str):
            raise TypeError("email must be a string or None.")

        if self.mobile is not None and not isinstance(self.mobile, str):
            raise TypeError("mobile must be a string or None.")