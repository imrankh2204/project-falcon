"""
Trade signal translation service for Project Falcon.

This module defines the application-layer service responsible for
translating a strategy-generated Signal into a broker-independent
TradeRequest.

The translator intentionally contains no trading logic, risk
management, portfolio inspection, or execution behaviour. Its sole
responsibility is constructing a valid TradeRequest from validated
inputs.
"""

from __future__ import annotations

from app.market.instrument import Instrument
from app.strategies.signal import Signal
from app.trading.trade_request import TradeRequest


class TradeSignalTranslator:
    """
    Application service responsible for translating strategy signals
    into executable trade requests.

    The translator is intentionally stateless and may be reused across
    multiple backtest or live trading sessions.
    """

    def translate(
        self,
        *,
        instrument: Instrument,
        signal: Signal,
        quantity: int,
    ) -> TradeRequest:
        """
        Translate a strategy signal into a TradeRequest.

        Parameters
        ----------
        instrument
            Instrument associated with the trade.

        signal
            Strategy-generated trading signal.

        quantity
            Number of units requested.

        Returns
        -------
        TradeRequest
            Broker-independent trade request.

        Raises
        ------
        TypeError
            If instrument or signal has an invalid type.

        ValueError
            If quantity is not greater than zero.
        """

        if not isinstance(instrument, Instrument):
            raise TypeError(
                "instrument must be an Instrument."
            )

        if not isinstance(signal, Signal):
            raise TypeError(
                "signal must be a Signal."
            )

        if quantity <= 0:
            raise ValueError(
                "quantity must be greater than zero."
            )

        return TradeRequest(
            instrument=instrument,
            signal=signal,
            quantity=quantity,
        )