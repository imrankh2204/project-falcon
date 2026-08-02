"""
Broker session validator for Project Falcon.

Determines whether a BrokerSession is currently usable.

The validator intentionally performs no broker communication.
"""

from __future__ import annotations

from app.live.broker_session import BrokerSession


class BrokerSessionValidator:
    """
    Validates broker sessions.
    """

    def validate(
        self,
        session: BrokerSession,
    ) -> bool:
        """
        Return True when the supplied session is active.
        """

        if not isinstance(
            session,
            BrokerSession,
        ):
            raise TypeError(
                "session must be a BrokerSession."
            )

        return session.is_active