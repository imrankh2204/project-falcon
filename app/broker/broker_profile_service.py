"""
Service for retrieving broker profile information as domain models.
"""

from __future__ import annotations

from app.live.exceptions import AuthenticationError

from .broker_profile import BrokerProfile
from .zerodha.kite_client import KiteClient


class BrokerProfileService:
    """
    Retrieve and map broker profile information into a broker-neutral model.
    """

    def __init__(self, client: KiteClient) -> None:
        if not isinstance(client, KiteClient):
            raise TypeError("client must be a KiteClient.")

        self._client = client

    def get_profile(self) -> BrokerProfile:
        """
        Return the current broker profile as a domain model.
        """

        try:
            profile_data = self._client.get_profile()
        except Exception as exc:
            raise AuthenticationError("Unable to retrieve broker profile.") from exc

        if not isinstance(profile_data, dict):
            raise AuthenticationError("Broker returned an invalid profile.")

        user_id = profile_data.get("user_id")
        if not isinstance(user_id, str) or not user_id.strip():
            raise AuthenticationError("Broker profile is missing a valid user id.")

        return BrokerProfile(
            broker_name=self._client.broker_name,
            user_id=user_id,
            user_name=profile_data.get("user_name"),
            email=profile_data.get("email"),
            mobile=profile_data.get("mobile"),
        )
