"""
Project Falcon

FAL-714-R3

Broker Account Snapshot Service

Coordinates broker account services to produce a unified,
immutable account snapshot.
"""

from __future__ import annotations

from app.broker.broker_account_snapshot import BrokerAccountSnapshot
from app.broker.broker_margin_service import BrokerMarginService
from app.broker.broker_profile_service import BrokerProfileService


class BrokerAccountSnapshotService:
    """
    Service responsible for producing a broker account snapshot.
    """

    def __init__(
        self,
        profile_service: BrokerProfileService,
        margin_service: BrokerMarginService,
    ) -> None:

        if not isinstance(
            profile_service,
            BrokerProfileService,
        ):
            raise TypeError(
                "profile_service must be a BrokerProfileService."
            )

        if not isinstance(
            margin_service,
            BrokerMarginService,
        ):
            raise TypeError(
                "margin_service must be a BrokerMarginService."
            )

        self._profile_service = profile_service
        self._margin_service = margin_service

    def get_snapshot(
        self,
    ) -> BrokerAccountSnapshot:
        """
        Retrieve the current broker account snapshot.
        """

        profile = self._profile_service.get_profile()

        margin = self._margin_service.get_margin()

        return BrokerAccountSnapshot(
            profile=profile,
            margin=margin,
        )