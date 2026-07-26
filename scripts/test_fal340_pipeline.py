"""
FAL-340 Optimization Pipeline End-to-End Validation.

Validates:
- Real OptimizationService composition.
- Real OptimizationWorkflow execution.
- Real OptimizationExecutor integration.
- BacktestApplicationFactory integration.
- BacktestApplication execution boundary.
- OptimizationReport creation.
- Deterministic behaviour.

This validation intentionally does NOT test:
- Parameter grid internals.
- Ranking algorithms.
- Export formatting.
- Broker integration.
- Live trading.
"""

from __future__ import annotations

from pathlib import Path

from app.backtest.backtest_config import (
    BacktestConfig,
)

from app.backtest.application_factory import (
    BacktestApplicationFactory,
)

from app.backtest.optimization.executor import (
    OptimizationExecutor,
)

from app.backtest.optimization.report_builder import (
    OptimizationReportBuilder,
)

from app.backtest.optimization.service import (
    OptimizationService,
)

from app.backtest.optimization.workflow import (
    OptimizationWorkflow,
)

from app.backtest.optimization.ranking import (
    RankingMetric,
)

from app.backtest.optimization.config import (
    OptimizationConfig,
)

from app.backtest.reporting.report import (
    BacktestReport,
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


TEST_CSV = Path(
    "data/fal340_pipeline_test.csv"
)


def create_test_csv() -> None:
    """
    Create deterministic historical candle dataset.
    """

    TEST_CSV.parent.mkdir(
        exist_ok=True
    )

    TEST_CSV.write_text(
        "\n".join(
            [
                "timestamp,open,high,low,close,volume",
                "2026-01-01 09:15:00,100,101,99,100.5,1000",
                "2026-01-01 09:20:00,100.5,102,100,101.5,1200",
                "2026-01-01 09:25:00,101.5,103,101,102.5,1400",
                "2026-01-01 09:30:00,102.5,104,102,103.5,1600",
                "2026-01-01 09:35:00,103.5,105,103,104.5,1800",
            ]
        ),
        encoding="utf-8",
    )


def build_service() -> OptimizationService:
    """
    Compose the real optimization pipeline.
    """

    config = BacktestConfig(
        csv_path=TEST_CSV,
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
            "data/fal340_output"
        ),
    )

    application_factory = (
        BacktestApplicationFactory(
            config=config
        )
    )

    executor = OptimizationExecutor(
        strategy_factory=StrategyFactory(),
        application_factory=application_factory,
    )

    workflow = OptimizationWorkflow(
        executor=executor,
        report_builder=OptimizationReportBuilder(),
    )

    return OptimizationService(
        workflow=workflow
    )


def build_config() -> OptimizationConfig:
    """
    Build deterministic optimization configuration.
    """

    return OptimizationConfig(
        fast_periods=(5,),
        slow_periods=(20,),
        ranking_metric=(
            RankingMetric.NET_PROFIT
        ),
        max_combinations=1,
    )


def test_pipeline_execution() -> None:

    service = build_service()

    report = service.run(
        build_config()
    )

    assert report.results

    assert isinstance(
        report.best_result.report,
        BacktestReport,
    )


def test_result_contents() -> None:

    service = build_service()

    report = service.run(
        build_config()
    )

    result = report.best_result

    assert (
        result.parameters.fast_period
        ==
        5
    )

    assert (
        result.parameters.slow_period
        ==
        20
    )


def test_determinism() -> None:

    service = build_service()

    first = service.run(
        build_config()
    )

    second = service.run(
        build_config()
    )

    assert first == second


def main() -> None:

    create_test_csv()

    test_pipeline_execution()

    test_result_contents()

    test_determinism()

    print("=" * 60)
    print(
        "FAL-340 Pipeline Validation Passed"
    )
    print("=" * 60)
    print()

    print(
        "Pipeline Composition : OK"
    )

    print(
        "Executor Integration : OK"
    )

    print(
        "Backtest Execution  : OK"
    )

    print(
        "Report Construction : OK"
    )

    print(
        "Determinism         : OK"
    )

    print()

    print("=" * 60)


if __name__ == "__main__":
    main()