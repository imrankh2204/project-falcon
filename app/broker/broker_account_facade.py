"""
Project Falcon

FAL-715-R1

Broker Account Facade

Provides a broker-neutral entry point for broker account information.
"""

from __future__ import annotations

from app.broker.broker_account_snapshot import (
    BrokerAccountSnapshot,
)
from app.broker.broker_account_snapshot_service import (
    BrokerAccountSnapshotService,
)


class BrokerAccountFacade:
    """
    Broker-neutral façade for account operations.
    """

    def __init__(
        self,
        snapshot_service: BrokerAccountSnapshotService,
    ) -> None:

        if not isinstance(
            snapshot_service,
            BrokerAccountSnapshotService,
        ):
            raise TypeError(
                "snapshot_service must be a BrokerAccountSnapshotService."
            )

        self._snapshot_service = snapshot_service

    def get_snapshot(
        self,
    ) -> BrokerAccountSnapshot:
        """
        Retrieve the current broker account snapshot.
        """

        return self._snapshot_service.get_snapshot()