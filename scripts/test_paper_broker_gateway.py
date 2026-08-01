"""
Project Falcon

FAL-530-R1

PaperBrokerGateway validation.

Validates:

- Authentication
- Quote registration
- Quote retrieval
- Order placement
- Order retrieval
- Order listing
- Position listing
- Logout
"""

from datetime import datetime

from app.live.order_request import OrderRequest
from app.live.order_type import OrderType
from app.live.product_type import ProductType
from app.live.quote import Quote
from app.live.transaction_type import TransactionType
from app.market.instrument import Instrument
from app.paper.paper_broker_gateway import (
    PaperBrokerGateway,
)


def main() -> None:

    gateway = PaperBrokerGateway()

    #
    # Authentication
    #
    session = gateway.authenticate()

    assert session is gateway.session()

    print("PASS: Authentication")

    instrument = Instrument(
        exchange="NFO",
        symbol="NIFTY",
        instrument_token=1,
        lot_size=50,
        tick_size=0.05,
        expiry=None,
        strike=25000,
        option_type=None,
    )

    #
    # Register quote
    #
    quote = Quote(
        instrument=instrument,
        last_price=250.50,
        bid=250.45,
        ask=250.55,
        volume=1000,
        timestamp=datetime.now(),
    )

    gateway.update_quote(
        quote,
    )

    returned_quote = gateway.quote(
        instrument,
    )

    assert returned_quote == quote

    print("PASS: Quote registration")

    #
    # Place order
    #
    order_request = OrderRequest(
        instrument=instrument,
        transaction_type=TransactionType.BUY,
        quantity=50,
        order_type=OrderType.MARKET,
        product_type=ProductType.MIS,
    )

    order = gateway.place_order(
        order_request,
    )

    assert order.quantity == 50
    assert order.average_price == 250.50

    print("PASS: Order placement")

    #
    # Retrieve order
    #
    retrieved = gateway.get_order(
        order.order_id,
    )

    assert retrieved == order

    print("PASS: Order retrieval")

    #
    # Order listing
    #
    orders = gateway.orders()

    assert len(orders) == 1

    print("PASS: Order listing")

    #
    # Position listing
    #
    positions = gateway.positions()

    assert len(positions) == 1

    print("PASS: Position listing")

    #
    # Logout
    #
    gateway.logout()

    assert gateway.session() is None

    print("PASS: Logout")

    print()
    print("FAL-530-R1 COMPLETE")


if __name__ == "__main__":
    main()