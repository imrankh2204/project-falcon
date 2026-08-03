"""
Unit tests for the Zerodha order mapper.
"""

from __future__ import annotations

from app.live.order_request import OrderRequest
from app.live.order_type import OrderType
from app.live.product_type import ProductType
from app.live.transaction_type import TransactionType
from app.broker.zerodha.order_mapper import OrderMapper
from app.market.instrument import Instrument


def test_to_kite_payload_contains_expected_fields() -> None:
    """
    OrderRequest should be translated into the payload expected by Kite.
    """

    instrument = Instrument(
        symbol="NIFTY 50",
        exchange="NSE",
        instrument_token=256265,
        lot_size=50,
        tick_size=0.05,
    )

    request = OrderRequest(
        instrument=instrument,
        transaction_type=TransactionType.BUY,
        quantity=100,
        order_type=OrderType.MARKET,
        product_type=ProductType.MIS,
    )

    payload = OrderMapper.to_kite(request)

    assert payload["tradingsymbol"] == "NIFTY 50"
    assert payload["exchange"] == "NSE"
    assert payload["transaction_type"] == "BUY"
    assert payload["quantity"] == 100
    assert payload["product"] == "MIS"
    assert payload["order_type"] == "MARKET"


def test_to_kite_includes_price_and_trigger_price() -> None:
    """
    Optional price fields should be preserved in the transport payload.
    """

    instrument = Instrument(
        symbol="BANKNIFTY",
        exchange="NSE",
        instrument_token=260105,
        lot_size=25,
        tick_size=0.05,
    )

    request = OrderRequest(
        instrument=instrument,
        transaction_type=TransactionType.SELL,
        quantity=50,
        order_type=OrderType.LIMIT,
        product_type=ProductType.CNC,
        price=100.0,
        trigger_price=99.5,
    )

    payload = OrderMapper.to_kite(request)

    assert payload["price"] == 100.0
    assert payload["trigger_price"] == 99.5
