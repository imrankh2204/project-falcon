"""
Trade signal translation service for Project Falcon.

Translates a strategy-generated Signal into a broker-independent
TradeRequest.

Responsibilities
----------------
- Translate strategy signals into TradeRequest objects.
- Remain stateless and deterministic.
- Preserve broker independence.

The translator intentionally does NOT implement:

- Strategy logic
- Risk validation
- Position sizing algorithms
- Broker communication
"""

from __future__ import annotations

from app.market.instrument import Instrument
from app.strategies.signal import Signal
from app.trading.trade_request import TradeRequest


class TradeSignalTranslator:
    """
    Stateless application service that translates trading signals into
    executable TradeRequest objects.
    """

    def __init__(
        self,
        *,
        default_quantity: int = 1,
    ) -> None:
        """
        Initialize the translator.

        Parameters
        ----------
        default_quantity
            Quantity assigned to every translated trade request.
        """

        if not isinstance(
            default_quantity,
            int,
        ):
            raise TypeError(
                "default_quantity must be an integer."
            )

        if default_quantity <= 0:
            raise ValueError(
                "default_quantity must be greater than zero."
            )

        self._default_quantity = (
            default_quantity
        )

    def translate(
        self,
        instrument: Instrument,
        signal: Signal,
    ) -> TradeRequest:
        """
        Translate a strategy signal into a TradeRequest.
        """

        if not isinstance(
            instrument,
            Instrument,
        ):
            raise TypeError(
                "instrument must be an Instrument."
            )

        if not isinstance(
            signal,
            Signal,
        ):
            raise TypeError(
                "signal must be a Signal."
            )

        return TradeRequest(
            instrument=instrument,
            signal=signal,
            quantity=self._default_quantity,
        )