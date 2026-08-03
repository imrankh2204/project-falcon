"""
Tests for the BrokerAccountFacade.
"""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from app.broker.broker_account_facade import BrokerAccountFacade
from app.broker.broker_account_snapshot import BrokerAccountSnapshot
from app.broker.broker_account_snapshot_service import (
    BrokerAccountSnapshotService,
)


def create_facade() -> BrokerAccountFacade:
    """
    Create a BrokerAccountFacade with mocked dependencies.
    """

    snapshot_service = MagicMock(
        spec=BrokerAccountSnapshotService,
    )

    snapshot = MagicMock(
        spec=BrokerAccountSnapshot,
    )

    snapshot_service.get_snapshot.return_value = snapshot

    return BrokerAccountFacade(
        snapshot_service=snapshot_service,
    )


def test_invalid_snapshot_service() -> None:
    """
    snapshot_service must be a BrokerAccountSnapshotService.
    """

    with pytest.raises(TypeError):
        BrokerAccountFacade(
            snapshot_service=object(),
        )


def test_get_snapshot() -> None:
    """
    The façade should return the snapshot from the service.
    """

    facade = create_facade()

    snapshot = facade.get_snapshot()

    assert isinstance(
        snapshot,
        BrokerAccountSnapshot,
    )


def test_snapshot_service_called_once() -> None:
    """
    The façade should delegate to the snapshot service.
    """

    snapshot_service = MagicMock(
        spec=BrokerAccountSnapshotService,
    )

    snapshot_service.get_snapshot.return_value = MagicMock(
        spec=BrokerAccountSnapshot,
    )

    facade = BrokerAccountFacade(
        snapshot_service=snapshot_service,
    )

    facade.get_snapshot()

    snapshot_service.get_snapshot.assert_called_once_with()


def test_snapshot_exception_propagates() -> None:
    """
    Exceptions from the snapshot service should propagate unchanged.
    """

    snapshot_service = MagicMock(
        spec=BrokerAccountSnapshotService,
    )

    snapshot_service.get_snapshot.side_effect = RuntimeError(
        "snapshot failure",
    )

    facade = BrokerAccountFacade(
        snapshot_service=snapshot_service,
    )

    with pytest.raises(RuntimeError):
        facade.get_snapshot()