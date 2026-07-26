"""
Validation suite for OptimizationService.
"""

from __future__ import annotations

from app.backtest.optimization.config import (
    OptimizationConfig,
)
from app.backtest.optimization.report import (
    OptimizationReport,
)
from app.backtest.optimization.report_builder import (
    OptimizationReportBuilder,
)
from app.backtest.optimization.result import (
    OptimizationResult,
)
from app.backtest.optimization.ranking import (
    RankingMetric,
)
from app.backtest.optimization.service import (
    OptimizationService,
)
from app.backtest.optimization.workflow import (
    OptimizationWorkflow,
)
from app.strategies.ema_parameters import (
    EMACrossoverParameters,
)


class FakeExecutor:
    """
    Deterministic executor stub.
    """

    def execute(
        self,
        parameters: EMACrossoverParameters,
    ) -> OptimizationResult:

        return OptimizationResult(
            parameters=parameters,
            report=None,
        )


class FakeReportBuilder(
    OptimizationReportBuilder
):
    """
    Deterministic report builder.
    """

    def build(
        self,
        results: tuple[
            OptimizationResult,
            ...,
        ],
    ) -> OptimizationReport:

        return OptimizationReport(
            results=results,
        )


def build_service() -> OptimizationService:

    workflow = OptimizationWorkflow(
        executor=FakeExecutor(),
        report_builder=FakeReportBuilder(),
    )

    return OptimizationService(
        workflow=workflow,
    )


def build_config() -> OptimizationConfig:

    return OptimizationConfig(
        fast_periods=(5, 9),
        slow_periods=(20, 30),
        ranking_metric=RankingMetric.NET_PROFIT,
    )


def test_configuration() -> None:

    service = build_service()

    report = service.run(
        build_config()
    )

    assert isinstance(
        report,
        OptimizationReport,
    )


def test_parameter_generation() -> None:

    report = build_service().run(
        build_config()
    )

    assert len(report.results) == 4


def test_workflow_execution() -> None:

    report = build_service().run(
        build_config()
    )

    assert all(
        isinstance(
            r,
            OptimizationResult,
        )
        for r in report.results
    )


def test_max_combinations() -> None:

    config = OptimizationConfig(
        fast_periods=(5, 9),
        slow_periods=(20, 30),
        ranking_metric=RankingMetric.NET_PROFIT,
        max_combinations=2,
    )

    report = build_service().run(
        config
    )

    assert len(report.results) == 2


def test_determinism() -> None:

    first = build_service().run(
        build_config()
    )

    second = build_service().run(
        build_config()
    )

    assert first.results == second.results


def main() -> None:

    test_configuration()
    test_parameter_generation()
    test_workflow_execution()
    test_max_combinations()
    test_determinism()

    print("=" * 60)
    print(
        "Optimization Service Validation Passed"
    )
    print("=" * 60)
    print()
    print("Configuration        : OK")
    print("Parameter Grid       : OK")
    print("Workflow             : OK")
    print("Report               : OK")
    print("Determinism          : OK")
    print()
    print("=" * 60)


if __name__ == "__main__":
    main()