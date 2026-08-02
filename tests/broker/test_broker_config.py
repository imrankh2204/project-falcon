"""
Unit tests for BrokerConfig.
"""

from __future__ import annotations

import pytest

from app.broker.broker_config import BrokerConfig


def test_valid_broker_config() -> None:
    """
    Verify a valid configuration is accepted.
    """

    config = BrokerConfig(
        broker_name="Zerodha",
        api_key="test-api-key",
        api_secret="test-secret",
        redirect_url="http://localhost:8000",
        sandbox=False,
    )

    assert config.broker_name == "Zerodha"
    assert config.api_key == "test-api-key"
    assert config.api_secret == "test-secret"
    assert config.redirect_url == "http://localhost:8000"
    assert config.sandbox is False


def test_empty_broker_name() -> None:
    """
    Empty broker name should raise ValueError.
    """

    with pytest.raises(ValueError):
        BrokerConfig(
            broker_name="",
            api_key="test-api-key",
        )


def test_empty_api_key() -> None:
    """
    Empty API key should raise ValueError.
    """

    with pytest.raises(ValueError):
        BrokerConfig(
            broker_name="Zerodha",
            api_key="",
        )


def test_invalid_broker_name_type() -> None:
    """
    broker_name must be a string.
    """

    with pytest.raises(TypeError):
        BrokerConfig(
            broker_name=123,
            api_key="test-api-key",
        )


def test_invalid_api_key_type() -> None:
    """
    api_key must be a string.
    """

    with pytest.raises(TypeError):
        BrokerConfig(
            broker_name="Zerodha",
            api_key=123,
        )


def test_invalid_api_secret_type() -> None:
    """
    api_secret must be a string or None.
    """

    with pytest.raises(TypeError):
        BrokerConfig(
            broker_name="Zerodha",
            api_key="test-api-key",
            api_secret=123,
        )


def test_invalid_redirect_url_type() -> None:
    """
    redirect_url must be a string or None.
    """

    with pytest.raises(TypeError):
        BrokerConfig(
            broker_name="Zerodha",
            api_key="test-api-key",
            redirect_url=123,
        )