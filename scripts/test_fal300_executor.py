"""
Validation suite for FAL-300 OptimizationExecutor.

Verifies:
- Strategy creation
- Application creation
- Backtest execution
- Optimization result construction
- Deterministic behaviour

This validation intentionally does NOT test:
- Historical replay
- Trading logic
- Ranking
- Exporting
"""

from __future__ import annotations

from dataclasses import dataclass

from app.backtest.optimization.executor import (
    OptimizationExecutor,
)
from app.backtest.optimization.result import (
    OptimizationResult,
)
from app.strategies.ema_parameters import (
    EMACrossoverParameters,
)


@dataclass(frozen=True, slots=True)
class DummyReport:
    """
    Minimal immutable report.
    """

    strategy_name: str


class DummyStrategy:
    """
    Strategy test double.
    """

    pass


class FakeStrategyFactory:
    """
    Deterministic strategy factory.
    """

    def create(
        self,
        parameters: EMACrossoverParameters,
    ) -> DummyStrategy:

        return DummyStrategy()


class DummyApplication:
    """
    Executable application stub.
    """

    def run(self) -> DummyReport:

        return DummyReport(
            strategy_name="EMA"
        )


class FakeApplicationFactory:
    """
    Deterministic BacktestApplicationFactory stub.
    """

    def create(
        self,
        strategy,
    ) -> DummyApplication:

        return DummyApplication()


def build_executor() -> OptimizationExecutor:

    executor = OptimizationExecutor.__new__(
        OptimizationExecutor
    )

    executor._strategy_factory = (
        FakeStrategyFactory()
    )

    executor._application_factory = (
        FakeApplicationFactory()
    )

    return executor


def test_execution() -> None:

    executor = build_executor()

    result = executor.execute(
        EMACrossoverParameters(
            fast_period=9,
            slow_period=21,
        )
    )

    assert isinstance(
        result,
        OptimizationResult,
    )

    assert (
        result.report.strategy_name
        == "EMA"
    )


def test_determinism() -> None:

    executor = build_executor()

    first = executor.execute(
        EMACrossoverParameters(
            fast_period=9,
            slow_period=21,
        )
    )

    second = executor.execute(
        EMACrossoverParameters(
            fast_period=9,
            slow_period=21,
        )
    )

    assert first == second


def main() -> None:

    test_execution()
    test_determinism()

    print("=" * 60)
    print(
        "FAL-300 Executor Validation Passed"
    )
    print("=" * 60)
    print()
    print("Execution     : OK")
    print("Determinism   : OK")
    print()
    print("=" * 60)


if __name__ == "__main__":
    main()