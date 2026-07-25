"""
Validation script for the Project Falcon execution cost model.

This script performs standalone validation of ExecutionCostModel.

Validation Coverage
-------------------
- Default zero-cost model
- Commission calculation
- Slippage calculation
- Total cost calculation
- Constructor validation
- Method validation
- Deterministic behavior
"""

from __future__ import annotations

from app.backtest.execution_cost_model import ExecutionCostModel


def test_default_model() -> None:
    model = ExecutionCostModel()

    assert model.commission(100_000.0) == 0.0
    assert model.slippage(50) == 0.0
    assert (
        model.total_cost(
            trade_value=100_000.0,
            quantity=50,
        )
        == 0.0
    )


def test_commission() -> None:
    model = ExecutionCostModel(
        commission_rate=0.001,
    )

    assert model.commission(100_000.0) == 100.0


def test_slippage() -> None:
    model = ExecutionCostModel(
        slippage_per_unit=0.05,
    )

    assert model.slippage(50) == 2.5


def test_total_cost() -> None:
    model = ExecutionCostModel(
        commission_rate=0.001,
        slippage_per_unit=0.05,
    )

    expected = 100.0 + 2.5

    assert (
        model.total_cost(
            trade_value=100_000.0,
            quantity=50,
        )
        == expected
    )


def test_constructor_validation() -> None:
    try:
        ExecutionCostModel(
            commission_rate=-0.1,
        )
        raise AssertionError(
            "Negative commission accepted."
        )
    except ValueError:
        pass

    try:
        ExecutionCostModel(
            slippage_per_unit=-1.0,
        )
        raise AssertionError(
            "Negative slippage accepted."
        )
    except ValueError:
        pass

    try:
        ExecutionCostModel(
            commission_rate="bad",  # type: ignore[arg-type]
        )
        raise AssertionError(
            "Invalid commission type accepted."
        )
    except TypeError:
        pass

    try:
        ExecutionCostModel(
            slippage_per_unit="bad",  # type: ignore[arg-type]
        )
        raise AssertionError(
            "Invalid slippage type accepted."
        )
    except TypeError:
        pass


def test_method_validation() -> None:
    model = ExecutionCostModel()

    try:
        model.commission(-1.0)
        raise AssertionError(
            "Negative trade value accepted."
        )
    except ValueError:
        pass

    try:
        model.slippage(-1)
        raise AssertionError(
            "Negative quantity accepted."
        )
    except ValueError:
        pass


def test_determinism() -> None:
    model = ExecutionCostModel(
        commission_rate=0.001,
        slippage_per_unit=0.05,
    )

    first = model.total_cost(
        trade_value=75_000.0,
        quantity=25,
    )

    second = model.total_cost(
        trade_value=75_000.0,
        quantity=25,
    )

    assert first == second


def main() -> None:
    test_default_model()
    test_commission()
    test_slippage()
    test_total_cost()
    test_constructor_validation()
    test_method_validation()
    test_determinism()

    print("=" * 60)
    print("Execution Cost Model Validation Passed")
    print("=" * 60)
    print()

    print("Default Model      : OK")
    print("Commission         : OK")
    print("Slippage           : OK")
    print("Total Cost         : OK")
    print("Validation         : OK")
    print("Determinism        : OK")
    print()

    print("=" * 60)


if __name__ == "__main__":
    main()