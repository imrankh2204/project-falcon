"""
Unit tests for BrokerSessionValidator.
"""

from __future__ import annotations

from datetime import datetime
from datetime import timedelta

import pytest

from app.broker.broker_session_validator import (
    BrokerSessionValidator,
)
from app.live.broker_session import BrokerSession
from app.live.session_status import SessionStatus


def create_session() -> BrokerSession:
    """
    Create a valid authenticated session.
    """

    return BrokerSession(
        broker_name="Zerodha",
        user_id="AB1234",
        access_token="token",
        authenticated_at=datetime.now(),
    )


def test_valid_session() -> None:
    """
    Active sessions validate successfully.
    """

    validator = BrokerSessionValidator()

    assert validator.validate(
        create_session()
    )


def test_invalid_type() -> None:
    """
    Validator rejects invalid objects.
    """

    validator = BrokerSessionValidator()

    with pytest.raises(TypeError):
        validator.validate(123)


def test_disconnected_session() -> None:
    """
    Disconnected sessions are invalid.
    """

    validator = BrokerSessionValidator()

    session = create_session().with_status(
        SessionStatus.DISCONNECTED,
    )

    assert not validator.validate(
        session,
    )


def test_failed_session() -> None:
    """
    Failed sessions are invalid.
    """

    validator = BrokerSessionValidator()

    session = create_session().with_status(
        SessionStatus.FAILED,
    )

    assert not validator.validate(
        session,
    )


def test_expired_session() -> None:
    """
    Expired sessions are invalid.
    """

    validator = BrokerSessionValidator()

    session = BrokerSession(
        broker_name="Zerodha",
        user_id="AB1234",
        access_token="token",
        authenticated_at=datetime.now(),
        expires_at=datetime.now() - timedelta(minutes=1),
    )

    assert not validator.validate(
        session,
    )


def test_session_without_expiry() -> None:
    """
    Sessions without expiry remain valid.
    """

    validator = BrokerSessionValidator()

    assert validator.validate(
        create_session(),
    )