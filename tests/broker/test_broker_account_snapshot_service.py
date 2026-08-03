"""
Tests for the BrokerAccountSnapshotService.
"""

from __future__ import annotations

from decimal import Decimal
from unittest.mock import MagicMock

import pytest

from app.broker.broker_account_snapshot import BrokerAccountSnapshot
from app.broker.broker_account_snapshot_service import (
    BrokerAccountSnapshotService,
)
from app.broker.broker_margin import BrokerMargin
from app.broker.broker_margin_service import BrokerMarginService
from app.broker.broker_profile import BrokerProfile
from app.broker.broker_profile_service import BrokerProfileService


def create_profile() -> BrokerProfile:
    """
    Create a valid BrokerProfile.
    """

    return BrokerProfile(
        broker_name="zerodha",
        user_id="AB1234",
        user_name="Project Falcon",
        email="falcon@example.com",
        mobile="9999999999",
    )


def create_margin() -> BrokerMargin:
    """
    Create a valid BrokerMargin.
    """

    return BrokerMargin(
        available_cash=Decimal("100000"),
        utilised_cash=Decimal("5000"),
        opening_balance=Decimal("105000"),
        payin=Decimal("0"),
        span_margin=Decimal("2500"),
        exposure_margin=Decimal("1500"),
        option_premium=Decimal("1000"),
        total_margin=Decimal("5000"),
    )


def create_service() -> BrokerAccountSnapshotService:
    """
    Create a BrokerAccountSnapshotService with mocked dependencies.
    """

    profile_service = MagicMock(spec=BrokerProfileService)
    margin_service = MagicMock(spec=BrokerMarginService)

    profile_service.get_profile.return_value = create_profile()
    margin_service.get_margin.return_value = create_margin()

    return BrokerAccountSnapshotService(
        profile_service=profile_service,
        margin_service=margin_service,
    )


def test_invalid_profile_service() -> None:
    """
    profile_service must be a BrokerProfileService.
    """

    with pytest.raises(TypeError):
        BrokerAccountSnapshotService(
            profile_service=object(),
            margin_service=MagicMock(spec=BrokerMarginService),
        )


def test_invalid_margin_service() -> None:
    """
    margin_service must be a BrokerMarginService.
    """

    with pytest.raises(TypeError):
        BrokerAccountSnapshotService(
            profile_service=MagicMock(spec=BrokerProfileService),
            margin_service=object(),
        )


def test_get_snapshot() -> None:
    """
    Service should return a BrokerAccountSnapshot.
    """

    service = create_service()

    snapshot = service.get_snapshot()

    assert isinstance(
        snapshot,
        BrokerAccountSnapshot,
    )

    assert snapshot.profile.user_id == "AB1234"

    assert snapshot.margin.available_cash == Decimal(
        "100000"
    )


def test_get_snapshot_calls_dependencies() -> None:
    """
    Both dependent services should be called exactly once.
    """

    profile_service = MagicMock(spec=BrokerProfileService)
    margin_service = MagicMock(spec=BrokerMarginService)

    profile_service.get_profile.return_value = create_profile()
    margin_service.get_margin.return_value = create_margin()

    service = BrokerAccountSnapshotService(
        profile_service=profile_service,
        margin_service=margin_service,
    )

    service.get_snapshot()

    profile_service.get_profile.assert_called_once_with()

    margin_service.get_margin.assert_called_once_with()


def test_profile_exception_propagates() -> None:
    """
    Exceptions from BrokerProfileService should propagate unchanged.
    """

    profile_service = MagicMock(spec=BrokerProfileService)
    margin_service = MagicMock(spec=BrokerMarginService)

    profile_service.get_profile.side_effect = RuntimeError(
        "profile failure",
    )

    service = BrokerAccountSnapshotService(
        profile_service=profile_service,
        margin_service=margin_service,
    )

    with pytest.raises(RuntimeError):
        service.get_snapshot()


def test_margin_exception_propagates() -> None:
    """
    Exceptions from BrokerMarginService should propagate unchanged.
    """

    profile_service = MagicMock(spec=BrokerProfileService)
    margin_service = MagicMock(spec=BrokerMarginService)

    profile_service.get_profile.return_value = create_profile()

    margin_service.get_margin.side_effect = RuntimeError(
        "margin failure",
    )

    service = BrokerAccountSnapshotService(
        profile_service=profile_service,
        margin_service=margin_service,
    )

    with pytest.raises(RuntimeError):
        service.get_snapshot()