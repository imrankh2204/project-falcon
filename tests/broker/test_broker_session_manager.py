"""
Unit tests for BrokerSessionManager.
"""

from __future__ import annotations

from datetime import datetime

import pytest

from app.broker.broker_session_manager import (
    BrokerSessionManager,
)
from app.live.broker_session import BrokerSession
from app.live.exceptions import AuthenticationError


def create_session() -> BrokerSession:
    return BrokerSession(
        broker_name="Zerodha",
        user_id="AB1234",
        access_token="token",
        authenticated_at=datetime.now(),
    )


def test_set_and_get_session() -> None:
    manager = BrokerSessionManager()

    session = create_session()

    manager.set_session(session)

    assert manager.get_session() is session


def test_has_session_initially_false() -> None:
    manager = BrokerSessionManager()

    assert manager.has_session is False


def test_has_session_after_set() -> None:
    manager = BrokerSessionManager()

    manager.set_session(create_session())

    assert manager.has_session is True


def test_clear_session() -> None:
    manager = BrokerSessionManager()

    manager.set_session(create_session())

    manager.clear_session()

    assert manager.has_session is False


def test_get_without_session() -> None:
    manager = BrokerSessionManager()

    with pytest.raises(AuthenticationError):
        manager.get_session()


def test_invalid_session_type() -> None:
    manager = BrokerSessionManager()

    with pytest.raises(TypeError):
        manager.set_session(123)