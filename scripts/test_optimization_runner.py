"""
Optimization runner validation for Project Falcon.

Validates deterministic optimization execution using lightweight test
doubles.

Validation coverage:
    - Parameter grid generation
    - Invalid parameter filtering
    - Runner execution
    - Deterministic ordering
"""

from __future__ import annotations

from dataclasses import dataclass

from app.backtest.optimization.parameter_grid import ParameterGrid
from app.backtest.optimization.runner import OptimizationRunner


@dataclass(frozen=True, slots=True)
class DummyReport:
    """
    Minimal immutable report used for validation.
    """

    strategy_name: str


class DummyApplication:
    """
    Minimal BacktestApplication test double.
    """

    def __init__(
        self,
        name: str,
    ) -> None:
        self._name = name

    def run(self) -> DummyReport:
        return DummyReport(
            strategy_name=self._name,
        )


def application_factory(parameters):
    """
    Deterministic application factory.
    """

    return DummyApplication(
        f"{parameters.fast_period}-{parameters.slow_period}"
    )


def test_parameter_generation() -> None:

    grid = ParameterGrid(
        fast_periods=[5, 9],
        slow_periods=[20, 30],
    )

    assert len(grid) == 4


def test_invalid_combinations() -> None:

    grid = ParameterGrid(
        fast_periods=[20, 30],
        slow_periods=[10, 20],
    )

    assert len(grid) == 0


def test_runner_execution() -> None:

    grid = ParameterGrid(
        fast_periods=[5],
        slow_periods=[20, 30],
    )

    results = OptimizationRunner().run(
        parameter_grid=grid,
        application_factory=application_factory,
    )

    assert len(results) == 2

    assert (
        results[0].report.strategy_name
        == "5-20"
    )

    assert (
        results[1].report.strategy_name
        == "5-30"
    )


def test_determinism() -> None:

    grid = ParameterGrid(
        fast_periods=[5, 9],
        slow_periods=[20],
    )

    runner = OptimizationRunner()

    run_one = runner.run(
        parameter_grid=grid,
        application_factory=application_factory,
    )

    run_two = runner.run(
        parameter_grid=grid,
        application_factory=application_factory,
    )

    assert run_one == run_two


def main() -> None:

    test_parameter_generation()
    test_invalid_combinations()
    test_runner_execution()
    test_determinism()

    print("=" * 60)
    print("Optimization Runner Validation Passed")
    print("=" * 60)
    print()
    print("Parameter Grid    : OK")
    print("Filtering         : OK")
    print("Runner            : OK")
    print("Determinism       : OK")
    print()
    print("=" * 60)


if __name__ == "__main__":
    main()