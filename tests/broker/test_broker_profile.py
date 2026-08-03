"""
Unit tests for BrokerProfile.
"""

from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from app.broker.broker_profile import BrokerProfile


def test_valid_profile() -> None:
    """
    A valid profile can be created with broker-neutral fields.
    """

    profile = BrokerProfile(
        broker_name="Zerodha",
        user_id="user-123",
        user_name="Falcon User",
        email="falcon@example.com",
        mobile="9999999999",
    )

    assert profile.broker_name == "Zerodha"
    assert profile.user_id == "user-123"
    assert profile.user_name == "Falcon User"
    assert profile.email == "falcon@example.com"
    assert profile.mobile == "9999999999"


def test_profile_is_immutable() -> None:
    """
    Profile instances should remain immutable after creation.
    """

    profile = BrokerProfile(
        broker_name="Zerodha",
        user_id="user-123",
    )

    with pytest.raises(FrozenInstanceError):
        profile.user_id = "other-user"


def test_invalid_profile_values() -> None:
    """
    Invalid profile values should be rejected.
    """

    with pytest.raises(TypeError):
        BrokerProfile(
            broker_name=123,
            user_id="user-123",
        )

    with pytest.raises(ValueError):
        BrokerProfile(
            broker_name="",
            user_id="user-123",
        )

    with pytest.raises(TypeError):
        BrokerProfile(
            broker_name="Zerodha",
            user_id=123,
        )
