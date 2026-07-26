"""
Validation script for FAL-280 Optimization Execution.

Validates:

- StrategyFactory integration.
- OptimizationExecutor execution.
- BacktestApplicationFactory isolation.
- Deterministic optimization results.
- OptimizationResult generation.

This script intentionally does NOT test:

- Strategy logic
- Indicator calculations
- Ranking logic
- Reporting formatting
"""

from __future__ import annotations

from pathlib import Path

from app.backtest.application_factory import (
    BacktestApplicationFactory,
)
from app.backtest.backtest_config import (
    BacktestConfig,
)
from app.backtest.optimization.executor import (
    OptimizationExecutor,
)
from app.backtest.optimization.result import (
    OptimizationResult,
)
from app.market.instrument import Instrument
from app.market.timeframe import TimeFrame
from app.strategies.ema_parameters import (
    EMACrossoverParameters,
)
from app.strategies.strategy_factory import (
    StrategyFactory,
)


def build_config() -> BacktestConfig:
    """
    Build deterministic test configuration.
    """

    return BacktestConfig(
        csv_path=Path(
            "data/historical/sample.csv"
        ),
        instrument=Instrument(
            exchange="NSE",
            symbol="NIFTY",
            instrument_token=0,
            lot_size=50,
            tick_size=0.05,
        ),
        timeframe=TimeFrame.FIVE_MINUTES,
        quantity=50,
        output_directory=Path(
            "data/reports"
        ),
    )


def build_executor() -> OptimizationExecutor:
    """
    Build optimization executor.
    """

    config = build_config()

    application_factory = (
        BacktestApplicationFactory(
            config=config,
        )
    )

    strategy_factory = StrategyFactory()

    return OptimizationExecutor(
        strategy_factory=strategy_factory,
        application_factory=application_factory,
    )


def test_execution() -> OptimizationResult:
    """
    Validate one optimization execution.
    """

    executor = build_executor()

    parameters = EMACrossoverParameters(
        fast_period=9,
        slow_period=21,
    )

    result = executor.execute(
        parameters
    )

    assert isinstance(
        result,
        OptimizationResult,
    )

    assert result.parameters == parameters

    assert result.report is not None

    return result


def test_determinism() -> None:
    """
    Validate repeated execution produces same output.
    """

    executor = build_executor()

    parameters = EMACrossoverParameters(
        fast_period=9,
        slow_period=21,
    )

    first = executor.execute(
        parameters
    )

    second = executor.execute(
        parameters
    )

    assert (
        first.report.performance.net_profit
        ==
        second.report.performance.net_profit
    )

    assert (
        first.report.performance.trade_count
        ==
        second.report.performance.trade_count
    )


def main() -> None:
    """
    Execute FAL-280 validation suite.
    """

    test_execution()

    test_determinism()

    print("=" * 60)
    print(
        "Optimization Execution Validation Passed"
    )
    print("=" * 60)
    print()

    print(
        "Strategy Factory       : OK"
    )
    print(
        "Executor               : OK"
    )
    print(
        "Application Factory    : OK"
    )
    print(
        "Optimization Result    : OK"
    )
    print(
        "Determinism            : OK"
    )
    print()

    print("=" * 60)


if __name__ == "__main__":
    main()