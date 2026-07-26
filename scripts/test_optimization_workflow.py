"""
Validation suite for OptimizationWorkflow.

Verifies:
- Parameter execution coordination.
- Multiple parameter handling.
- Report aggregation.
- Executor integration.
- Deterministic ordering.

This validation intentionally does NOT test:
- Strategy logic
- Backtest execution
- Ranking logic
- Console rendering
"""

from __future__ import annotations

from app.backtest.optimization.report import (
    OptimizationReport,
)
from app.backtest.optimization.report_builder import (
    OptimizationReportBuilder,
)
from app.backtest.optimization.result import (
    OptimizationResult,
)
from app.backtest.optimization.workflow import (
    OptimizationWorkflow,
)
from app.strategies.ema_parameters import (
    EMACrossoverParameters,
)


class FakeExecutor:
    """
    Deterministic executor stub used for workflow validation.
    """

    def __init__(self) -> None:
        self.executed: list[
            EMACrossoverParameters
        ] = []

    def execute(
        self,
        parameters: EMACrossoverParameters,
    ) -> OptimizationResult:
        """
        Record execution and return deterministic result.
        """

        self.executed.append(
            parameters
        )

        return OptimizationResult(
            parameters=parameters,
            report=None,
        )


class FakeReportBuilder:
    """
    Deterministic report builder stub.
    """

    def build(
        self,
        results: tuple[
            OptimizationResult,
            ...,
        ],
    ) -> OptimizationReport:
        """
        Aggregate results into a validation report.
        """

        return OptimizationReport(
            results=results,
        )


def _parameters(
    fast: int,
    slow: int,
) -> EMACrossoverParameters:

    return EMACrossoverParameters(
        fast_period=fast,
        slow_period=slow,
    )


def test_single_parameter_execution() -> None:

    executor = FakeExecutor()

    workflow = OptimizationWorkflow(
        executor=executor,
        report_builder=FakeReportBuilder(),
    )

    parameter = (
        _parameters(
            9,
            21,
        ),
    )

    report = workflow.run(
        parameter
    )

    assert len(report.results) == 1

    assert executor.executed == list(
        parameter
    )


def test_multiple_parameters() -> None:

    executor = FakeExecutor()

    workflow = OptimizationWorkflow(
        executor=executor,
        report_builder=FakeReportBuilder(),
    )

    parameters = (
        _parameters(
            5,
            20,
        ),
        _parameters(
            9,
            21,
        ),
        _parameters(
            12,
            30,
        ),
    )

    report = workflow.run(
        parameters
    )

    assert len(report.results) == 3

    assert executor.executed == list(
        parameters
    )


def test_report_aggregation() -> None:

    workflow = OptimizationWorkflow(
        executor=FakeExecutor(),
        report_builder=FakeReportBuilder(),
    )

    report = workflow.run(
        (
            _parameters(
                9,
                21,
            ),
        )
    )

    assert isinstance(
        report,
        OptimizationReport,
    )

    assert len(
        report.results
    ) == 1


def test_determinism() -> None:

    parameters = (
        _parameters(
            5,
            20,
        ),
        _parameters(
            9,
            21,
        ),
    )

    first = OptimizationWorkflow(
        executor=FakeExecutor(),
        report_builder=FakeReportBuilder(),
    ).run(parameters)

    second = OptimizationWorkflow(
        executor=FakeExecutor(),
        report_builder=FakeReportBuilder(),
    ).run(parameters)

    assert first.results == second.results


def test_empty_parameters() -> None:

    workflow = OptimizationWorkflow(
        executor=FakeExecutor(),
        report_builder=FakeReportBuilder(),
    )

    try:
        workflow.run(
            tuple()
        )
    except ValueError:
        return

    raise AssertionError(
        "Expected ValueError for empty parameters."
    )


def main() -> None:

    test_single_parameter_execution()

    test_multiple_parameters()

    test_report_aggregation()

    test_determinism()

    test_empty_parameters()

    print("=" * 60)
    print(
        "Optimization Workflow Validation Passed"
    )
    print("=" * 60)
    print("")
    print(
        "Single Parameter Execution : OK"
    )
    print(
        "Multiple Parameters        : OK"
    )
    print(
        "Report Aggregation         : OK"
    )
    print(
        "Executor Integration       : OK"
    )
    print(
        "Determinism                : OK"
    )
    print("")
    print("=" * 60)


if __name__ == "__main__":
    main()