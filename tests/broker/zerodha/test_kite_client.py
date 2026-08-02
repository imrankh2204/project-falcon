"""
Unit tests for the KiteClient adapter.

These tests verify that the Falcon adapter correctly delegates
operations to the Kite Connect SDK while keeping the SDK
encapsulated behind the adapter boundary.
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from app.broker.broker_config import BrokerConfig
from app.broker.zerodha.kite_client import KiteClient


def create_config(
    api_secret: str | None = "test-secret",
) -> BrokerConfig:
    """
    Create a valid BrokerConfig for testing.
    """

    return BrokerConfig(
        broker_name="Zerodha",
        api_key="test-api-key",
        api_secret=api_secret,
        redirect_url="http://localhost:8000",
    )


@patch("app.broker.zerodha.kite_client.KiteConnect")
def test_construct_client(mock_kite) -> None:
    """
    Verify the SDK client is constructed correctly.
    """

    config = create_config()

    KiteClient(config)

    mock_kite.assert_called_once_with(
        api_key=config.api_key,
    )


def test_invalid_config_type() -> None:
    """
    Constructor should reject invalid configuration objects.
    """

    with pytest.raises(TypeError):
        KiteClient(123)


@patch("app.broker.zerodha.kite_client.KiteConnect")
def test_broker_name(mock_kite) -> None:
    """
    Verify broker_name returns the configured broker.
    """

    client = KiteClient(create_config())

    assert client.broker_name == "Zerodha"


@patch("app.broker.zerodha.kite_client.KiteConnect")
def test_login_url(mock_kite) -> None:
    """
    Verify login_url delegates to the SDK.
    """

    sdk = mock_kite.return_value
    sdk.login_url.return_value = (
        "https://kite.trade/connect/login"
    )

    client = KiteClient(create_config())

    url = client.login_url()

    assert (
        url
        == "https://kite.trade/connect/login"
    )

    sdk.login_url.assert_called_once_with()


@patch("app.broker.zerodha.kite_client.KiteConnect")
def test_generate_session(mock_kite) -> None:
    """
    Verify generate_session delegates correctly.
    """

    sdk = mock_kite.return_value

    sdk.generate_session.return_value = {
        "access_token": "token"
    }

    config = create_config()

    client = KiteClient(config)

    result = client.generate_session(
        "request-token"
    )

    assert result == {
        "access_token": "token"
    }

    sdk.generate_session.assert_called_once_with(
        request_token="request-token",
        api_secret=config.api_secret,
    )


@patch("app.broker.zerodha.kite_client.KiteConnect")
def test_generate_session_empty_request_token(
    mock_kite,
) -> None:
    """
    Empty request token should fail.
    """

    client = KiteClient(create_config())

    with pytest.raises(ValueError):
        client.generate_session("")


@patch("app.broker.zerodha.kite_client.KiteConnect")
def test_generate_session_invalid_request_token(
    mock_kite,
) -> None:
    """
    Request token must be a string.
    """

    client = KiteClient(create_config())

    with pytest.raises(TypeError):
        client.generate_session(123)


@patch("app.broker.zerodha.kite_client.KiteConnect")
def test_generate_session_requires_api_secret(
    mock_kite,
) -> None:
    """
    API secret is required.
    """

    client = KiteClient(
        create_config(api_secret=None)
    )

    with pytest.raises(ValueError):
        client.generate_session(
            "request-token"
        )


@patch("app.broker.zerodha.kite_client.KiteConnect")
def test_set_access_token(mock_kite) -> None:
    """
    Verify access token delegation.
    """

    sdk = mock_kite.return_value

    sdk.set_access_token = MagicMock()

    client = KiteClient(create_config())

    client.set_access_token(
        "access-token"
    )

    sdk.set_access_token.assert_called_once_with(
        "access-token"
    )


@patch("app.broker.zerodha.kite_client.KiteConnect")
def test_empty_access_token(
    mock_kite,
) -> None:
    """
    Empty access token should fail.
    """

    client = KiteClient(create_config())

    with pytest.raises(ValueError):
        client.set_access_token("")


@patch("app.broker.zerodha.kite_client.KiteConnect")
def test_invalid_access_token_type(
    mock_kite,
) -> None:
    """
    Access token must be a string.
    """

    client = KiteClient(create_config())

    with pytest.raises(TypeError):
        client.set_access_token(123)


def test_login_url_returns_sdk_value() -> None:
    """
    login_url delegates to the SDK.
    """

    sdk = MagicMock()

    sdk.login_url.return_value = (
        "https://kite.trade/connect/login"
    )

    with patch(
        "app.broker.zerodha.kite_client.KiteConnect",
        return_value=sdk,
    ):
        config = BrokerConfig(
            broker_name="Zerodha",
            api_key="test-api-key",
        )

        client = KiteClient(config)

        assert (
            client.login_url()
            == "https://kite.trade/connect/login"
        )

        sdk.login_url.assert_called_once_with()