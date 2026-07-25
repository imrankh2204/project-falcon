"""
Validation script for ExecutionPriceModel.

Run:

    python -m scripts.test_execution_price_model
"""

from __future__ import annotations

from app.backtest.execution_price_model import (
    ExecutionPriceModel,
)


def test_default_model() -> None:
    """
    Verify zero-slippage behaviour.
    """

    model = ExecutionPriceModel()

    assert model.buy_price(100.0) == 100.0
    assert model.sell_price(100.0) == 100.0


def test_buy_slippage() -> None:
    """
    BUY executions should include positive slippage.
    """

    model = ExecutionPriceModel(
        slippage_per_unit=0.5,
    )

    price = model.buy_price(100.0)

    assert price == 100.5


def test_sell_slippage() -> None:
    """
    SELL executions should include negative slippage.
    """

    model = ExecutionPriceModel(
        slippage_per_unit=0.5,
    )

    price = model.sell_price(100.0)

    assert price == 99.5


def test_deterministic() -> None:
    """
    Model must always produce deterministic prices.
    """

    model = ExecutionPriceModel(
        slippage_per_unit=0.25,
    )

    buy_1 = model.buy_price(250.0)
    buy_2 = model.buy_price(250.0)

    sell_1 = model.sell_price(250.0)
    sell_2 = model.sell_price(250.0)

    assert buy_1 == buy_2
    assert sell_1 == sell_2


def test_validation() -> None:
    """
    Verify constructor validation.
    """

    try:
        ExecutionPriceModel(
            slippage_per_unit=-0.1,
        )
    except ValueError:
        pass
    else:
        raise AssertionError(
            "Negative slippage must raise ValueError."
        )


def test_market_price_validation() -> None:
    """
    Verify market price validation.
    """

    model = ExecutionPriceModel()

    try:
        model.buy_price(-1.0)
    except ValueError:
        pass
    else:
        raise AssertionError(
            "Negative BUY price must raise ValueError."
        )

    try:
        model.sell_price(-1.0)
    except ValueError:
        pass
    else:
        raise AssertionError(
            "Negative SELL price must raise ValueError."
        )


def main() -> None:
    """
    Execute all validations.
    """

    test_default_model()
    test_buy_slippage()
    test_sell_slippage()
    test_deterministic()
    test_validation()
    test_market_price_validation()

    print("=" * 60)
    print("Execution Price Model Validation Passed")
    print("=" * 60)
    print()
    print("Default Model      : OK")
    print("Buy Slippage       : OK")
    print("Sell Slippage      : OK")
    print("Validation         : OK")
    print("Price Validation   : OK")
    print("Determinism        : OK")
    print()
    print("=" * 60)


if __name__ == "__main__":
    main()