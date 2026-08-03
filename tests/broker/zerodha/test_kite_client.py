"""
Unit tests for the KiteClient adapter.

These tests verify that the Falcon adapter correctly delegates
operations to the Kite Connect SDK while keeping the SDK
encapsulated behind the adapter boundary.
"""

from __future__ import annotations

from unittest.mock import MagicMock
from unittest.mock import patch

import pytest

from app.broker.broker_config import BrokerConfig
from app.broker.zerodha.kite_client import KiteClient
from app.broker.exceptions import BrokerAuthenticationError


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
    Create a KiteClient backed by a mocked SDK.
    """

    sdk = MagicMock()

    with patch(
        "app.broker.zerodha.kite_client.KiteConnect",
        return_value=sdk,
    ):
        client = KiteClient(
            create_config(),
        )

    return client


@patch("app.broker.zerodha.kite_client.KiteConnect")
def test_construct_client(
    mock_kite,
) -> None:
    """
    Verify SDK construction.
    """

    config = create_config()

    KiteClient(config)

    mock_kite.assert_called_once_with(
        api_key=config.api_key,
    )


def test_invalid_config_type() -> None:
    """
    Constructor validates configuration.
    """

    with pytest.raises(TypeError):
        KiteClient(123)


@patch("app.broker.zerodha.kite_client.KiteConnect")
def test_broker_name(
    mock_kite,
) -> None:
    """
    Broker name is exposed.
    """

    client = KiteClient(
        create_config(),
    )

    assert (
        client.broker_name
        == "Zerodha"
    )


@patch("app.broker.zerodha.kite_client.KiteConnect")
def test_login_url(
    mock_kite,
) -> None:
    """
    Login URL delegates to SDK.
    """

    sdk = mock_kite.return_value

    sdk.login_url.return_value = (
        "https://kite.trade/connect/login"
    )

    client = KiteClient(
        create_config(),
    )

    assert (
        client.login_url()
        == "https://kite.trade/connect/login"
    )

    sdk.login_url.assert_called_once_with()


@patch("app.broker.zerodha.kite_client.KiteConnect")
def test_generate_session(
    mock_kite,
) -> None:
    """
    Session generation delegates correctly.
    """

    sdk = mock_kite.return_value

    sdk.generate_session.return_value = {
        "access_token": "token",
    }

    config = create_config()

    client = KiteClient(config)

    result = client.generate_session(
        request_token="request-token",
        api_secret="test-secret",
    )

    assert result == {
        "access_token": "token",
    }

    sdk.generate_session.assert_called_once_with(
        request_token="request-token",
        api_secret="test-secret",
    )


@patch("app.broker.zerodha.kite_client.KiteConnect")
def test_set_access_token(
    mock_kite,
) -> None:
    """
    Access token delegates correctly.
    """

    sdk = mock_kite.return_value

    client = KiteClient(
        create_config(),
    )

    client.set_access_token(
        "access-token",
    )

    sdk.set_access_token.assert_called_once_with(
        "access-token",
    )


def test_get_profile() -> None:
    """
    Profile is retrieved.
    """

    client = create_client()

    client._client.profile.return_value = {
        "user_name": "Falcon User",
    }

    profile = client.get_profile()

    assert (
        profile["user_name"]
        == "Falcon User"
    )

    client._client.profile.assert_called_once_with()


def test_invalid_profile_response() -> None:
    """
    Invalid SDK response becomes BrokerAuthenticationError.
    """

    client = create_client()

    client._client.profile.return_value = []

    with pytest.raises(
        BrokerAuthenticationError,
    ):
        client.get_profile()


def test_profile_exception_translation() -> None:
    """
    SDK exceptions are translated.
    """

    client = create_client()

    client._client.profile.side_effect = RuntimeError(
        "SDK failure",
    )

    with pytest.raises(
        BrokerAuthenticationError,
    ):
        client.get_profile()