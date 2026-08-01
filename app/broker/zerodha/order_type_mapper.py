"""
Maps Falcon order types to Kite order types.
"""

from __future__ import annotations

from app.live.order_type import OrderType


class OrderTypeMapper:
    """
    Translate Falcon order types into Kite values.
    """

    _MAP: dict[OrderType, str] = {
        OrderType.MARKET: "MARKET",
        OrderType.LIMIT: "LIMIT",
        OrderType.SL: "SL",
        OrderType.SL_MARKET: "SL-M",
    }

    @classmethod
    def to_kite(
        cls,
        order_type: OrderType,
    ) -> str:
        """
        Convert Falcon order type into Kite order type.
        """

        if not isinstance(
            order_type,
            OrderType,
        ):
            raise TypeError(
                "order_type must be an OrderType."
            )

        return cls._MAP[order_type]