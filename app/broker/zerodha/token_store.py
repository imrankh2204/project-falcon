"""
Token storage abstraction for Zerodha authentication.

This module isolates authenticated session persistence from the
authentication workflow.

Responsibilities
----------------
- Persist authenticated broker sessions.
- Load previously stored broker sessions.
- Remove persisted sessions.

Concrete implementations may choose any persistence mechanism
(files, encrypted storage, databases, operating-system credential
stores, etc.).

The interface intentionally remains independent from any specific
storage implementation.
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from app.live.broker_session import BrokerSession


class TokenStore(ABC):
    """
    Abstract authenticated-session persistence contract.
    """

    @abstractmethod
    def load(
        self,
    ) -> BrokerSession | None:
        """
        Load a previously persisted broker session.

        Returns
        -------
        BrokerSession | None
            Persisted authenticated session, or None if unavailable.
        """

    @abstractmethod
    def save(
        self,
        session: BrokerSession,
    ) -> None:
        """
        Persist an authenticated broker session.

        Parameters
        ----------
        session
            Immutable authenticated broker session.
        """

    @abstractmethod
    def clear(
        self,
    ) -> None:
        """
        Remove any persisted broker session.
        """