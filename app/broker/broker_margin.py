"""
Project Falcon

FAL-714-R2

Broker Margin Domain

Immutable broker-neutral margin domain model.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True, slots=True)
class BrokerMargin:
    """
    Immutable broker-neutral representation of account margin.
    """

    available_cash: Decimal
    utilised_cash: Decimal
    opening_balance: Decimal
    payin: Decimal
    span_margin: Decimal
    exposure_margin: Decimal
    option_premium: Decimal
    total_margin: Decimal

    def __post_init__(self) -> None:
        for name, value in (
            ("available_cash", self.available_cash),
            ("utilised_cash", self.utilised_cash),
            ("opening_balance", self.opening_balance),
            ("payin", self.payin),
            ("span_margin", self.span_margin),
            ("exposure_margin", self.exposure_margin),
            ("option_premium", self.option_premium),
            ("total_margin", self.total_margin),
        ):
            if not isinstance(value, Decimal):
                raise TypeError(f"{name} must be a Decimal.")

            if value < Decimal("0"):
                raise ValueError(f"{name} cannot be negative.")
