"""
Tests for the BrokerAccountSnapshot domain model.
"""

from __future__ import annotations

from dataclasses import FrozenInstanceError
from decimal import Decimal

import pytest

from app.broker.broker_account_snapshot import BrokerAccountSnapshot
from app.broker.broker_margin import BrokerMargin
from app.broker.broker_profile import BrokerProfile


def create_profile() -> BrokerProfile:
    """
    Create a valid BrokerProfile for testing.
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
    Create a valid BrokerMargin for testing.
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


def test_create_snapshot() -> None:
    """
    A valid snapshot should be created successfully.
    """

    snapshot = BrokerAccountSnapshot(
        profile=create_profile(),
        margin=create_margin(),
    )

    assert snapshot.profile.user_id == "AB1234"

    assert snapshot.margin.available_cash == Decimal(
        "100000"
    )


def test_invalid_profile_type() -> None:
    """
    profile must be a BrokerProfile.
    """

    with pytest.raises(
        TypeError,
    ):
        BrokerAccountSnapshot(
            profile=object(),
            margin=create_margin(),
        )


def test_invalid_margin_type() -> None:
    """
    margin must be a BrokerMargin.
    """

    with pytest.raises(
        TypeError,
    ):
        BrokerAccountSnapshot(
            profile=create_profile(),
            margin=object(),
        )


def test_snapshot_is_immutable() -> None:
    """
    Snapshot should be immutable.
    """

    snapshot = BrokerAccountSnapshot(
        profile=create_profile(),
        margin=create_margin(),
    )

    with pytest.raises(
        FrozenInstanceError,
    ):
        snapshot.profile = create_profile()