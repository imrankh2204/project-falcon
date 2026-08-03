"""
Unit tests for BrokerProfileService.
"""

from __future__ import annotations

import pytest

from app.broker.broker_profile import BrokerProfile
from app.broker.broker_profile_service import BrokerProfileService
from app.broker.zerodha.kite_client import KiteClient
from app.live.exceptions import AuthenticationError


class StubKiteClient(KiteClient):
    """
    Minimal test double for the broker client.
    """

    def __init__(self) -> None:
        self._profile_payload: dict | None = None
        self._error: Exception | None = None
        self._broker_name = "Zerodha"

    @property
    def broker_name(self) -> str:
        return self._broker_name

    def get_profile(self) -> dict:
        if self._error is not None:
            raise self._error

        if self._profile_payload is None:
            return {}

        return self._profile_payload


def test_get_profile_maps_response() -> None:
    """
    The service should map raw broker response data into a domain model.
    """

    client = StubKiteClient()
    client._profile_payload = {
        "user_id": "user-123",
        "user_name": "Falcon User",
        "email": "falcon@example.com",
        "mobile": "9999999999",
    }

    service = BrokerProfileService(client)
    profile = service.get_profile()

    assert isinstance(profile, BrokerProfile)
    assert profile.broker_name == "Zerodha"
    assert profile.user_id == "user-123"
    assert profile.user_name == "Falcon User"
    assert profile.email == "falcon@example.com"
    assert profile.mobile == "9999999999"


def test_get_profile_propagates_authentication_errors() -> None:
    """
    Broker authentication failures should be preserved.
    """

    client = StubKiteClient()
    client._error = AuthenticationError("broker failure")

    service = BrokerProfileService(client)

    with pytest.raises(AuthenticationError):
        service.get_profile()


def test_get_profile_requires_user_id() -> None:
    """
    Missing user identifiers should be rejected.
    """

    client = StubKiteClient()
    client._profile_payload = {
        "user_name": "Falcon User",
    }

    service = BrokerProfileService(client)

    with pytest.raises(AuthenticationError):
        service.get_profile()
