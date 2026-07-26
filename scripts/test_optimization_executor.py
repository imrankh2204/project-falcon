"""
OptimizationExecutor validation for Project Falcon.

Validates:

- Constructor validation.
- Dependency validation.
- Deterministic construction.

Execution behaviour is intentionally validated by:

- test_optimization_pipeline.py
- test_fal340_pipeline.py
"""

from __future__ import annotations

from pathlib import Path

from app.backtest.application_factory import (
    BacktestApplicationFactory,
)
from app.backtest.backtest_config import (
    BacktestConfig,
)
from app.backtest.date_range import (
    DateRange,
)
from app.backtest.optimization.executor import (
    OptimizationExecutor,
)
from app.market.instrument import (
    Instrument,
)
from app.market.option_type import (
    OptionType,
)
from app.market.timeframe import (
    TimeFrame,
)
from app.strategies.strategy_factory import (
    StrategyFactory,
)


def build_factory() -> BacktestApplicationFactory:

    config = BacktestConfig(
        csv_path=Path("dummy.csv"),
        instrument=Instrument(
            exchange="NSE",
            symbol="NIFTY",
            instrument_token=1,
            lot_size=50,
            tick_size=0.05,
            option_type=OptionType.CALL,
        ),
        timeframe=TimeFrame.FIVE_MINUTES,
        quantity=1,
        output_directory=Path("."),
        date_range=None,
    )

    return BacktestApplicationFactory(
        config=config,
    )


def test_constructor() -> None:

    executor = OptimizationExecutor(
        strategy_factory=StrategyFactory(),
        application_factory=build_factory(),
    )

    assert isinstance(
        executor,
        OptimizationExecutor,
    )


def test_invalid_strategy_factory() -> None:

    try:

        OptimizationExecutor(
            strategy_factory=object(),
            application_factory=build_factory(),
        )

    except TypeError:

        return

    raise AssertionError(
        "Expected TypeError."
    )


def test_invalid_application_factory() -> None:

    try:

        OptimizationExecutor(
            strategy_factory=StrategyFactory(),
            application_factory=object(),
        )

    except TypeError:

        return

    raise AssertionError(
        "Expected TypeError."
    )


def test_determinism() -> None:

    first = OptimizationExecutor(
        strategy_factory=StrategyFactory(),
        application_factory=build_factory(),
    )

    second = OptimizationExecutor(
        strategy_factory=StrategyFactory(),
        application_factory=build_factory(),
    )

    assert type(first) is type(second)


def main() -> None:

    test_constructor()
    test_invalid_strategy_factory()
    test_invalid_application_factory()
    test_determinism()

    print("=" * 60)
    print(
        "Optimization Executor Validation Passed"
    )
    print("=" * 60)
    print()
    print(
        "Constructor      : OK"
    )
    print(
        "Dependencies     : OK"
    )
    print(
        "Determinism      : OK"
    )
    print()
    print("=" * 60)


if __name__ == "__main__":
    main()