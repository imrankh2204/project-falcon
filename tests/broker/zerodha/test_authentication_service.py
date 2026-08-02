"""
Unit tests for the AuthenticationService.

These tests verify that SDK session data is translated into
Falcon's immutable BrokerSession without leaking SDK objects.
"""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from app.broker.broker_config import BrokerConfig
from app.broker.zerodha.authentication_service import (
    AuthenticationService,
)
from app.broker.zerodha.kite_client import KiteClient
from app.live.broker_session import BrokerSession
from app.live.session_status import SessionStatus


def create_config() -> BrokerConfig:
    """
    Create a valid BrokerConfig.
    """

    return BrokerConfig(
        broker_name="Zerodha",
        api_key="test-api-key",
        api_secret="test-secret",
        redirect_url="http://localhost:8000",
    )


def create_client() -> KiteClient:
    """
    Create a mocked KiteClient.
    """

    client = MagicMock(spec=KiteClient)

    client.generate_session.return_value = {
        "access_token": "access-token",
        "user_id": "AB1234",
    }

    return client


def test_authenticate_returns_broker_session() -> None:
    """
    Successful authentication returns a BrokerSession.
    """

    service = AuthenticationService(
        create_config(),
        create_client(),
    )

    session = service.authenticate(
        "request-token"
    )

    assert isinstance(
        session,
        BrokerSession,
    )

    assert (
        session.broker_name
        == "Zerodha"
    )

    assert (
        session.user_id
        == "AB1234"
    )

    assert (
        session.access_token
        == "access-token"
    )

    assert (
        session.status
        is SessionStatus.AUTHENTICATED
    )


def test_generate_session_called() -> None:
    """
    Verify request token exchange.
    """

    client = create_client()

    service = AuthenticationService(
        create_config(),
        client,
    )

    service.authenticate(
        "request-token"
    )

    client.generate_session.assert_called_once_with(
        "request-token"
    )


def test_access_token_is_registered() -> None:
    """
    Verify SDK access token registration.
    """

    client = create_client()

    service = AuthenticationService(
        create_config(),
        client,
    )

    service.authenticate(
        "request-token"
    )

    client.set_access_token.assert_called_once_with(
        "access-token"
    )


def test_invalid_request_token_type() -> None:
    """
    Request token must be a string.
    """

    service = AuthenticationService(
        create_config(),
        create_client(),
    )

    with pytest.raises(TypeError):
        service.authenticate(123)


def test_empty_request_token() -> None:
    """
    Empty request token is rejected.
    """

    service = AuthenticationService(
        create_config(),
        create_client(),
    )

    with pytest.raises(ValueError):
        service.authenticate("")


def test_invalid_config_type() -> None:
    """
    Constructor validates BrokerConfig.
    """

    with pytest.raises(TypeError):
        AuthenticationService(
            123,
            create_client(),
        )


def test_invalid_client_type() -> None:
    """
    Constructor validates KiteClient.
    """

    with pytest.raises(TypeError):
        AuthenticationService(
            create_config(),
            123,
        )