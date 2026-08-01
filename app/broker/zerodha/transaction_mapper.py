"""
Maps Falcon transaction types to Kite transaction types.
"""

from __future__ import annotations

from app.live.transaction_type import TransactionType


class TransactionMapper:
    """
    Translate Falcon transaction types into Kite values.
    """

    _MAP: dict[TransactionType, str] = {
        TransactionType.BUY: "BUY",
        TransactionType.SELL: "SELL",
    }

    @classmethod
    def to_kite(
        cls,
        transaction_type: TransactionType,
    ) -> str:
        """
        Convert Falcon transaction type into Kite transaction type.
        """

        if not isinstance(
            transaction_type,
            TransactionType,
        ):
            raise TypeError(
                "transaction_type must be a TransactionType."
            )

        return cls._MAP[transaction_type]