"""
Unit tests for the AuthenticationService.

These tests verify that SDK session data is translated into
Falcon's immutable BrokerSession without leaking SDK objects.
"""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from app.broker.zerodha.authentication_service import (
    AuthenticationService,
)
from app.broker.zerodha.kite_client import KiteClient
from app.live.broker_session import BrokerSession
from app.live.exceptions import AuthenticationError
from app.live.session_status import SessionStatus


def create_client() -> KiteClient:
    """
    Create a mocked KiteClient.
    """

    client = MagicMock(
        spec=KiteClient,
    )

    client.broker_name = "Zerodha"

    client.generate_session.return_value = {
        "access_token": "access-token",
        "user_id": "AB1234",
    }

    return client


def test_authenticate_returns_broker_session() -> None:
    client = create_client()

    service = AuthenticationService(
        client,
    )

    session = service.authenticate(
        "request-token",
        "api-secret",
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

    client = create_client()

    service = AuthenticationService(
        client,
    )

    service.authenticate(
        "request-token",
        "api-secret",
    )

    client.generate_session.assert_called_once_with(
        request_token="request-token",
        api_secret="api-secret",
    )


def test_access_token_registered() -> None:

    client = create_client()

    service = AuthenticationService(
        client,
    )

    service.authenticate(
        "request-token",
        "api-secret",
    )

    client.set_access_token.assert_called_once_with(
        "access-token"
    )


def test_invalid_request_token_type() -> None:

    service = AuthenticationService(
        create_client(),
    )

    with pytest.raises(TypeError):
        service.authenticate(
            123,
            "api-secret",
        )


def test_empty_request_token() -> None:

    service = AuthenticationService(
        create_client(),
    )

    with pytest.raises(ValueError):
        service.authenticate(
            "",
            "api-secret",
        )


def test_invalid_api_secret_type() -> None:

    service = AuthenticationService(
        create_client(),
    )

    with pytest.raises(TypeError):
        service.authenticate(
            "request-token",
            123,
        )


def test_empty_api_secret() -> None:

    service = AuthenticationService(
        create_client(),
    )

    with pytest.raises(ValueError):
        service.authenticate(
            "request-token",
            "",
        )


def test_invalid_client_type() -> None:

    with pytest.raises(TypeError):
        AuthenticationService(
            123,
        )


def test_invalid_session_type() -> None:

    client = create_client()

    client.generate_session.return_value = []

    service = AuthenticationService(
        client,
    )

    with pytest.raises(AuthenticationError):
        service.authenticate(
            "request-token",
            "api-secret",
        )


def test_missing_access_token() -> None:

    client = create_client()

    client.generate_session.return_value = {
        "user_id": "AB1234",
    }

    service = AuthenticationService(
        client,
    )

    with pytest.raises(AuthenticationError):
        service.authenticate(
            "request-token",
            "api-secret",
        )


def test_missing_user_id() -> None:

    client = create_client()

    client.generate_session.return_value = {
        "access_token": "access-token",
    }

    service = AuthenticationService(
        client,
    )

    with pytest.raises(AuthenticationError):
        service.authenticate(
            "request-token",
            "api-secret",
        )


def test_sdk_exception_translated() -> None:

    client = create_client()

    client.generate_session.side_effect = RuntimeError(
        "SDK failure"
    )

    service = AuthenticationService(
        client,
    )

    with pytest.raises(AuthenticationError):
        service.authenticate(
            "request-token",
            "api-secret",
        )