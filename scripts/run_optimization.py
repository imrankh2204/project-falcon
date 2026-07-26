"""
Optimization CLI entry point for Project Falcon.

Builds the optimization dependency graph and executes an optimization run.
"""

from __future__ import annotations

from app.backtest.optimization.config import (
    OptimizationConfig,
)
from app.backtest.optimization.executor import (
    OptimizationExecutor,
)
from app.backtest.optimization.report_builder import (
    OptimizationReportBuilder,
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
from app.backtest.reporting.builder import (
    ReportBuilder,
)
from app.core.optimization_application import (
    OptimizationApplication,
)
from app.strategies.strategy_factory import (
    StrategyFactory,
)


def build_application() -> OptimizationApplication:
    """
    Construct the optimization application.
    """

    strategy_factory = StrategyFactory()

    report_builder = ReportBuilder()

    executor = OptimizationExecutor(
        strategy_factory=strategy_factory,
        backtest_runner=lambda strategy: None,
        report_builder=report_builder,
    )

    workflow = OptimizationWorkflow(
        executor=executor,
        report_builder=OptimizationReportBuilder(),
    )

    service = OptimizationService(
        workflow=workflow,
    )

    config = OptimizationConfig(
        fast_periods=(5, 9, 12),
        slow_periods=(20, 21, 30),
        ranking_metric=RankingMetric.NET_PROFIT,
    )

    return OptimizationApplication(
        config=config,
        service=service,
    )


def main() -> None:
    """
    CLI entry point.

    The full optimization execution wiring will be completed in the
    remaining FAL-220 implementation. For now, this validates dependency
    construction.
    """

    application = build_application()

    print("=" * 60)
    print("Project Falcon Optimization CLI")
    print("=" * 60)
    print()
    print("Application :", application.__class__.__name__)
    print("Status      : Ready")
    print()
    print("=" * 60)


if __name__ == "__main__":
    main()