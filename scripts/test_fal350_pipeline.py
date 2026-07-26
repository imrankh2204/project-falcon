"""
FAL-350 Walk-Forward End-to-End Pipeline Validation.

Validates:
- WalkForwardService orchestration.
- WalkForwardEngine execution.
- OptimizationService integration.
- Strategy parameter propagation.
- Validation backtest execution.
- WalkForwardResult construction.
- Deterministic behaviour.

This validation intentionally does NOT test:
- Strategy logic.
- Indicator calculations.
- Ranking algorithms.
- Export formatting.
- Broker integration.
"""

from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path

from app.backtest.backtest_factory_bridge import (
    BacktestFactoryBridge,
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

from app.backtest.optimization.ranking import (
    RankingMetric,
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

from app.backtest.walk_forward.configuration_bridge import (
    WalkForwardConfigurationBridge,
)

from app.backtest.walk_forward.config import (
    WalkForwardConfig,
)

from app.backtest.walk_forward.engine import (
    WalkForwardEngine,
)

from app.backtest.walk_forward.service import (
    WalkForwardService,
)

from app.backtest.walk_forward.window import (
    WalkForwardWindow,
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
    "data/fal350_pipeline_test.csv"
)


def create_test_csv() -> None:
    """
    Create deterministic historical data.

    The generated dataset covers:
    - Training window:
        2026-01-01 -> 2026-01-10

    - Validation window:
        2026-01-11 -> 2026-01-15

    Generates realistic 5-minute market candles:
    - NSE-style session
    - 09:15 to 15:30
    - 75 candles per trading day
    """

    TEST_CSV.parent.mkdir(
        exist_ok=True
    )

    rows = [
        "timestamp,open,high,low,close,volume"
    ]

    price = 100.0

    trading_day = datetime(
        2026,
        1,
        1,
    )

    for _ in range(15):

        session_time = datetime(
            trading_day.year,
            trading_day.month,
            trading_day.day,
            9,
            15,
        )

        for _ in range(75):

            rows.append(
                (
                    f"{session_time:%Y-%m-%d %H:%M:%S},"
                    f"{price},"
                    f"{price + 1},"
                    f"{price - 1},"
                    f"{price + 0.5},"
                    "1000"
                )
            )

            price += 0.5

            session_time += timedelta(
                minutes=5
            )

        trading_day += timedelta(
            days=1
        )

    TEST_CSV.write_text(
        "\n".join(rows),
        encoding="utf-8",
    )


def build_backtest_config() -> BacktestConfig:

    return BacktestConfig(
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
            "data/fal350_output"
        ),
    )


def build_optimization_service() -> OptimizationService:

    from app.backtest.application_factory import (
        BacktestApplicationFactory,
    )

    application_factory = (
        BacktestApplicationFactory(
            config=build_backtest_config()
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
        workflow=workflow,
    )


def build_engine() -> WalkForwardEngine:

    base_optimization = OptimizationConfig(
        fast_periods=(5,),
        slow_periods=(20,),
        ranking_metric=RankingMetric.NET_PROFIT,
        max_combinations=1,
    )

    base_backtest = build_backtest_config()

    return WalkForwardEngine(
        optimization_service=(
            build_optimization_service()
        ),
        configuration_bridge=(
            WalkForwardConfigurationBridge(
                optimization_config=base_optimization,
                backtest_config=base_backtest,
            )
        ),
        backtest_factory_bridge=(
            BacktestFactoryBridge()
        ),
    )


def build_window() -> WalkForwardWindow:

    return WalkForwardWindow(
        training_start=datetime(
            2026,
            1,
            1,
            9,
            15,
        ),
        training_end=datetime(
            2026,
            1,
            10,
            15,
        ),
        validation_start=datetime(
            2026,
            1,
            11,
            9,
            15,
        ),
        validation_end=datetime(
            2026,
            1,
            15,
            15,
        ),
    )


def test_pipeline() -> None:

    service = WalkForwardService(
        engine=build_engine()
    )

    result = service.run(
        config=WalkForwardConfig(
            training_days=10,
            validation_days=5,
            step_days=5,
        ),
        windows=[
            build_window()
        ],
    )

    assert (
        result.iteration_count
        ==
        1
    )

    iteration = result.iterations[0]

    assert (
        iteration.optimization_result
        is not None
    )

    assert (
        iteration.validation_report
        is not None
    )


def test_determinism() -> None:

    service = WalkForwardService(
        engine=build_engine()
    )

    first = service.run(
        config=WalkForwardConfig(
            training_days=10,
            validation_days=5,
            step_days=5,
        ),
        windows=[
            build_window()
        ],
    )

    second = service.run(
        config=WalkForwardConfig(
            training_days=10,
            validation_days=5,
            step_days=5,
        ),
        windows=[
            build_window()
        ],
    )

    assert first == second


def main() -> None:

    create_test_csv()

    test_pipeline()

    test_determinism()

    print("=" * 60)
    print(
        "FAL-350 Pipeline Validation Passed"
    )
    print("=" * 60)
    print()

    print(
        "WalkForward Service : OK"
    )

    print(
        "Engine Execution   : OK"
    )

    print(
        "Optimization Flow  : OK"
    )

    print(
        "Validation Backtest: OK"
    )

    print(
        "Result Construction: OK"
    )

    print(
        "Determinism        : OK"
    )

    print()

    print("=" * 60)


if __name__ == "__main__":
    main()