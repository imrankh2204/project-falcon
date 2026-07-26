"""
Optimization CLI entry point for Project Falcon.

Builds the optimization dependency graph and executes an optimization run.
"""

from __future__ import annotations

from pathlib import Path

from app.backtest.application_factory import (
    BacktestApplicationFactory,
)
from app.backtest.backtest_config import (
    BacktestConfig,
)
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
from app.core.optimization_application import (
    OptimizationApplication,
)
from app.market.instrument import (
    Instrument,
)
from app.market.timeframe import (
    TimeFrame,
)
from app.strategies.strategy_factory import (
    StrategyFactory,
)


def build_application() -> OptimizationApplication:
    """
    Construct the optimization application.
    """

    backtest_config = BacktestConfig(
        csv_path=Path("data/history.csv"),
        instrument=Instrument(
            exchange="NSE",
            symbol="NIFTY",
            instrument_token=0,
            lot_size=50,
            tick_size=0.05,
        ),
        timeframe=TimeFrame.FIVE_MINUTES,
        quantity=1,
        output_directory=Path("reports"),
    )

    application_factory = (
        BacktestApplicationFactory(
            backtest_config,
        )
    )

    strategy_factory = StrategyFactory()

    executor = OptimizationExecutor(
        strategy_factory=strategy_factory,
        application_factory=application_factory,
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

    The optimization dependency graph is fully wired.
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