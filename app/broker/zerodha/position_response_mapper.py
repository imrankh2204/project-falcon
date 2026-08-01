"""
Maps Kite position payloads into Falcon BrokerPosition objects.

Responsibilities
----------------
- Convert Kite position payloads into immutable BrokerPosition objects.
- Remain broker independent.
- Perform deterministic payload translation.

The mapper intentionally does NOT implement:

- Broker SDK communication
- Repository lookups
- Session management
- Position synchronization
"""

from __future__ import annotations

from typing import Any

from app.live.broker_position import (
    BrokerPosition,
)
from app.market.instrument import (
    Instrument,
)


class PositionResponseMapper:
    """
    Maps Kite position payloads into BrokerPosition.
    """

    @staticmethod
    def from_kite(
        *,
        instrument: Instrument,
        payload: dict[str, Any],
    ) -> BrokerPosition:
        """
        Convert a Kite position payload into BrokerPosition.
        """

        if not isinstance(
            instrument,
            Instrument,
        ):
            raise TypeError(
                "instrument must be an Instrument."
            )

        if not isinstance(
            payload,
            dict,
        ):
            raise TypeError(
                "payload must be a dictionary."
            )

        return BrokerPosition(
            instrument=instrument,
            quantity=int(
                payload.get(
                    "quantity",
                    0,
                )
            ),
            average_price=float(
                payload.get(
                    "average_price",
                    0.0,
                )
            ),
            realized_pnl=float(
                payload.get(
                    "realised",
                    0.0,
                )
            ),
            unrealized_pnl=float(
                payload.get(
                    "unrealised",
                    0.0,
                )
            ),
        )