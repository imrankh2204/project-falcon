"""
Broker session manager.

Owns the authenticated BrokerSession for the running process.

This class intentionally performs no authentication and no broker
communication. It only stores and retrieves the current session.
"""

from __future__ import annotations

from app.live.broker_session import BrokerSession
from app.live.exceptions import AuthenticationError


class BrokerSessionManager:
    """
    Stores the authenticated broker session.
    """

    def __init__(self) -> None:
        self._session: BrokerSession | None = None

    def set_session(
        self,
        session: BrokerSession,
    ) -> None:
        """
        Store the authenticated session.
        """

        if not isinstance(
            session,
            BrokerSession,
        ):
            raise TypeError(
                "session must be a BrokerSession."
            )

        self._session = session

    def get_session(
        self,
    ) -> BrokerSession:
        """
        Return the authenticated session.
        """

        if self._session is None:
            raise AuthenticationError(
                "Broker session has not been established."
            )

        return self._session

    def clear_session(
        self,
    ) -> None:
        """
        Remove the current session.
        """

        self._session = None

    @property
    def has_session(
        self,
    ) -> bool:
        """
        Whether a session is currently stored.
        """

        return self._session is not None