"""
Project Falcon

FAL-714-R2

Broker Margin Service

Maps broker margin payloads into the immutable BrokerMargin domain model.
"""

from __future__ import annotations

from decimal import Decimal
from decimal import InvalidOperation

from app.broker.broker_margin import BrokerMargin
from app.broker.exceptions import BrokerError
from app.broker.zerodha.kite_client import KiteClient


class BrokerMarginService:
    """
    Service responsible for retrieving and validating broker margin details.
    """

    def __init__(
        self,
        client: KiteClient,
    ) -> None:

        if not isinstance(
            client,
            KiteClient,
        ):
            raise TypeError(
                "client must be a KiteClient."
            )

        self._client = client

    def get_margin(
        self,
    ) -> BrokerMargin:
        """
        Retrieve the current broker margin snapshot.
        """

        try:
            payload = self._client.get_margins()

        except BrokerError:
            raise

        except Exception as exc:
            raise BrokerError(
                "Unable to retrieve broker margins."
            ) from exc

        if not isinstance(
            payload,
            dict,
        ):
            raise TypeError(
                "Broker margin payload must be a dictionary."
            )

        equity = self._require_dict(
            payload,
            "equity",
        )

        available = self._require_dict(
            equity,
            "available",
        )

        utilised = self._require_dict(
            equity,
            "utilised",
        )

        return BrokerMargin(
            available_cash=self._to_decimal(
                available,
                "cash",
            ),
            utilised_cash=self._to_decimal(
                utilised,
                "debits",
            ),
            opening_balance=self._to_decimal(
                available,
                "opening_balance",
            ),
            payin=self._to_decimal(
                available,
                "payin",
            ),
            span_margin=self._to_decimal(
                utilised,
                "span",
            ),
            exposure_margin=self._to_decimal(
                utilised,
                "exposure",
            ),
            option_premium=self._to_decimal(
                utilised,
                "option_premium",
            ),
            total_margin=self._to_decimal(
                utilised,
                "total",
            ),
        )

    @staticmethod
    def _require_dict(
        payload: dict,
        key: str,
    ) -> dict:

        if key not in payload:
            raise ValueError(
                f"Missing required broker payload section '{key}'."
            )

        value = payload[key]

        if not isinstance(
            value,
            dict,
        ):
            raise TypeError(
                f"Broker payload section '{key}' must be a dictionary."
            )

        return value

    @staticmethod
    def _to_decimal(
        payload: dict,
        field: str,
    ) -> Decimal:

        if field not in payload:
            raise ValueError(
                f"Missing required broker field '{field}'."
            )

        value = payload[field]

        try:
            return Decimal(
                str(value),
            )

        except (
            InvalidOperation,
            TypeError,
            ValueError,
        ) as exc:
            raise ValueError(
                f"Invalid numeric value for broker field '{field}'."
            ) from exc