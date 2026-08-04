"""
Project Falcon

FAL-716-R1

Broker Session Recovery Service

Provides broker-neutral automatic session recovery for broker operations.

Responsibilities
----------------
- Execute broker operations.
- Detect authentication/session failures.
- Invoke session recovery.
- Retry the original operation once.

This service intentionally does NOT:
- Communicate with broker SDKs.
- Generate broker sessions.
- Store authentication tokens.
- Implement broker-specific logic.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import TypeVar

from app.live.exceptions import (
    AuthenticationError,
    SessionExpiredError,
)

T = TypeVar("T")


class BrokerSessionRecoveryService:
    """
    Broker-neutral session recovery coordinator.

    Executes broker operations while automatically recovering
    expired broker sessions when possible.
    """

    def __init__(
        self,
        recovery_callback: Callable[[], None],
    ) -> None:
        """
        Initialize the recovery service.

        Parameters
        ----------
        recovery_callback
            Callable responsible for recovering the broker session.
        """

        if not callable(
            recovery_callback,
        ):
            raise TypeError(
                "recovery_callback must be callable."
            )

        self._recovery_callback = recovery_callback

    def execute(
        self,
        operation: Callable[[], T],
    ) -> T:
        """
        Execute a broker operation.

        The operation is attempted once. If it fails because of an
        authentication or expired-session error, the configured
        recovery callback is invoked and the operation is retried
        exactly one additional time.

        Parameters
        ----------
        operation
            Broker operation to execute.

        Returns
        -------
        T
            Result returned by the broker operation.

        Raises
        ------
        AuthenticationError
            If recovery is unsuccessful.

        SessionExpiredError
            If the session remains invalid after recovery.

        Any other exception raised by the operation is propagated
        unchanged.
        """

        if not callable(
            operation,
        ):
            raise TypeError(
                "operation must be callable."
            )

        try:
            return operation()

        except (
            AuthenticationError,
            SessionExpiredError,
        ):
            self._recovery_callback()

            return operation()