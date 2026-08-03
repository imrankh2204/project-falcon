"""
Project Falcon

FAL-714-R3

Broker Account Snapshot Domain

Immutable broker-neutral account snapshot composed of
validated broker domain objects.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.broker.broker_margin import BrokerMargin
from app.broker.broker_profile import BrokerProfile


@dataclass(
    frozen=True,
    slots=True,
)
class BrokerAccountSnapshot:
    """
    Immutable broker-neutral account snapshot.

    Combines the broker profile and current margin state into a
    single domain object for consumption by higher-level services.
    """

    profile: BrokerProfile

    margin: BrokerMargin

    def __post_init__(
        self,
    ) -> None:

        if not isinstance(
            self.profile,
            BrokerProfile,
        ):
            raise TypeError(
                "profile must be a BrokerProfile."
            )

        if not isinstance(
            self.margin,
            BrokerMargin,
        ):
            raise TypeError(
                "margin must be a BrokerMargin."
            )