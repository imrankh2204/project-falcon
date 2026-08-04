"""
Unit tests for BrokerSessionRecoveryService.
"""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from app.broker.broker_session_recovery_service import (
    BrokerSessionRecoveryService,
)
from app.live.exceptions import (
    AuthenticationError,
    SessionExpiredError,
)


def test_constructor_accepts_callable() -> None:
    """
    Constructor should accept a callable recovery callback.
    """

    service = BrokerSessionRecoveryService(
        recovery_callback=lambda: None,
    )

    assert isinstance(
        service,
        BrokerSessionRecoveryService,
    )


def test_constructor_rejects_non_callable() -> None:
    """
    Constructor should reject non-callable callbacks.
    """

    with pytest.raises(
        TypeError,
    ):
        BrokerSessionRecoveryService(
            recovery_callback=123,
        )


def test_execute_requires_callable_operation() -> None:
    """
    execute() should require a callable operation.
    """

    service = BrokerSessionRecoveryService(
        recovery_callback=lambda: None,
    )

    with pytest.raises(
        TypeError,
    ):
        service.execute(
            123,
        )


def test_execute_success() -> None:
    """
    Successful operations should execute without recovery.
    """

    recovery = MagicMock()

    service = BrokerSessionRecoveryService(
        recovery_callback=recovery,
    )

    operation = MagicMock(
        return_value="success",
    )

    result = service.execute(
        operation,
    )

    assert result == "success"

    operation.assert_called_once()

    recovery.assert_not_called()


def test_authentication_error_recovers() -> None:
    """
    Authentication failures should trigger one recovery and retry.
    """

    recovery = MagicMock()

    operation = MagicMock(
        side_effect=[
            AuthenticationError(
                "expired",
            ),
            "success",
        ],
    )

    service = BrokerSessionRecoveryService(
        recovery_callback=recovery,
    )

    result = service.execute(
        operation,
    )

    assert result == "success"

    assert operation.call_count == 2

    recovery.assert_called_once()


def test_session_expired_recovers() -> None:
    """
    SessionExpiredError should trigger one recovery and retry.
    """

    recovery = MagicMock()

    operation = MagicMock(
        side_effect=[
            SessionExpiredError(
                "expired",
            ),
            "success",
        ],
    )

    service = BrokerSessionRecoveryService(
        recovery_callback=recovery,
    )

    result = service.execute(
        operation,
    )

    assert result == "success"

    assert operation.call_count == 2

    recovery.assert_called_once()


def test_authentication_failure_after_retry() -> None:
    """
    AuthenticationError after retry should propagate.
    """

    recovery = MagicMock()

    operation = MagicMock(
        side_effect=[
            AuthenticationError(
                "expired",
            ),
            AuthenticationError(
                "still expired",
            ),
        ],
    )

    service = BrokerSessionRecoveryService(
        recovery_callback=recovery,
    )

    with pytest.raises(
        AuthenticationError,
    ):
        service.execute(
            operation,
        )

    assert operation.call_count == 2

    recovery.assert_called_once()


def test_session_expired_after_retry() -> None:
    """
    SessionExpiredError after retry should propagate.
    """

    recovery = MagicMock()

    operation = MagicMock(
        side_effect=[
            SessionExpiredError(
                "expired",
            ),
            SessionExpiredError(
                "still expired",
            ),
        ],
    )

    service = BrokerSessionRecoveryService(
        recovery_callback=recovery,
    )

    with pytest.raises(
        SessionExpiredError,
    ):
        service.execute(
            operation,
        )

    assert operation.call_count == 2

    recovery.assert_called_once()


def test_other_exceptions_are_not_retried() -> None:
    """
    Non-authentication exceptions should propagate immediately.
    """

    recovery = MagicMock()

    operation = MagicMock(
        side_effect=ValueError(
            "boom",
        ),
    )

    service = BrokerSessionRecoveryService(
        recovery_callback=recovery,
    )

    with pytest.raises(
        ValueError,
    ):
        service.execute(
            operation,
        )

    operation.assert_called_once()

    recovery.assert_not_called()


def test_recovery_callback_exception_propagates() -> None:
    """
    Exceptions raised by the recovery callback should propagate.
    """

    recovery = MagicMock(
        side_effect=RuntimeError(
            "recovery failed",
        ),
    )

    operation = MagicMock(
        side_effect=AuthenticationError(
            "expired",
        ),
    )

    service = BrokerSessionRecoveryService(
        recovery_callback=recovery,
    )

    with pytest.raises(
        RuntimeError,
    ):
        service.execute(
            operation,
        )

    recovery.assert_called_once()

    assert operation.call_count == 1