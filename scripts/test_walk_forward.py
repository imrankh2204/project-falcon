"""
Walk-forward optimization validation for Project Falcon.

Validates:
- Configuration creation.
- Window validation.
- Engine execution.
- Service orchestration.
- Deterministic behaviour.

This validation intentionally avoids:
- CSV loading
- Historical replay
- Optimization execution
- Strategy logic
- Reporting exporters
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from app.backtest.advanced_performance_snapshot import (
    AdvancedPerformanceSnapshot,
)
from app.backtest.backtest_config import (
    BacktestConfig,
)
from app.backtest.backtest_factory_bridge import (
    BacktestFactoryBridge,
)
from app.backtest.equity_curve_snapshot import (
    EquityCurveSnapshot,
)
from app.backtest.optimization.config import (
    OptimizationConfig,
)
from app.backtest.optimization.report import (
    OptimizationReport,
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
from app.backtest.performance_snapshot import (
    PerformanceSnapshot,
)
from app.backtest.reporting.report import (
    BacktestReport,
)
from app.backtest.walk_forward.config import (
    WalkForwardConfig,
)
from app.backtest.walk_forward.configuration_bridge import (
    WalkForwardConfigurationBridge,
)
from app.backtest.walk_forward.engine import (
    WalkForwardEngine,
)
from app.backtest.walk_forward.result import (
    WalkForwardResult,
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
from app.strategies.ema_parameters import (
    EMACrossoverParameters,
)


def build_report() -> BacktestReport:
    """
    Construct a deterministic BacktestReport.
    """

    instrument = Instrument(
        exchange="NSE",
        symbol="NIFTY",
        instrument_token=0,
        lot_size=50,
        tick_size=0.05,
    )

    performance = PerformanceSnapshot(
        trade_count=1,
        winning_trades=1,
        losing_trades=0,
        win_rate=100.0,
        gross_profit=100.0,
        gross_loss=0.0,
        net_profit=100.0,
        average_win=100.0,
        average_loss=0.0,
        largest_win=100.0,
        largest_loss=0.0,
    )

    advanced = AdvancedPerformanceSnapshot(
        profit_factor=1.0,
        expectancy=100.0,
        sharpe_ratio=1.0,
        sortino_ratio=1.0,
    )

    equity = EquityCurveSnapshot(
        points=(),
        peak_equity=0.0,
        maximum_drawdown=0.0,
        maximum_drawdown_percentage=0.0,
    )

    return BacktestReport(
        instrument=instrument,
        strategy_name="EMACrossoverStrategy",
        start_time=datetime(
            2026,
            3,
            1,
            9,
            15,
            tzinfo=timezone.utc,
        ),
        end_time=datetime(
            2026,
            3,
            20,
            15,
            30,
            tzinfo=timezone.utc,
        ),
        performance=performance,
        advanced_performance=advanced,
        equity_curve=equity,
    )


class DummyOptimizationService(
    OptimizationService,
):
    """
    Lightweight optimization service used only by validation.
    """

    def __init__(self) -> None:
        pass

    def run(
        self,
        _config,
    ) -> OptimizationReport:

        return OptimizationReport(
            results=(
                OptimizationResult(
                    parameters=EMACrossoverParameters(
                        fast_period=5,
                        slow_period=20,
                    ),
                    report=build_report(),
                ),
            )
        )


class DummyConfigurationBridge(
    WalkForwardConfigurationBridge,
):
    """
    Deterministic configuration bridge.
    """

    def __init__(self) -> None:

        instrument = Instrument(
            exchange="NSE",
            symbol="NIFTY",
            instrument_token=0,
            lot_size=50,
            tick_size=0.05,
        )

        optimization_config = OptimizationConfig(
            fast_periods=(5,),
            slow_periods=(20,),
            ranking_metric=RankingMetric.NET_PROFIT,
        )

        backtest_config = BacktestConfig(
            csv_path=Path("dummy.csv"),
            instrument=instrument,
            timeframe=TimeFrame.FIVE_MINUTES,
            quantity=50,
            output_directory=Path("."),
        )

        super().__init__(
            optimization_config=optimization_config,
            backtest_config=backtest_config,
        )


class DummyApplication:
    """
    Deterministic validation application.
    """

    def run(
        self,
    ) -> BacktestReport:

        return build_report()


class DummyFactory:
    """
    Deterministic application factory.
    """

    def create(
        self,
        _strategy,
    ) -> DummyApplication:

        return DummyApplication()


class DummyBacktestFactoryBridge(
    BacktestFactoryBridge,
):
    """
    Validation bridge.
    """

    def __init__(self) -> None:
        pass

    def create(
        self,
        _config,
    ) -> DummyFactory:

        return DummyFactory()


def build_engine() -> WalkForwardEngine:

    return WalkForwardEngine(
        optimization_service=DummyOptimizationService(),
        configuration_bridge=DummyConfigurationBridge(),
        backtest_factory_bridge=DummyBacktestFactoryBridge(),
    )


def build_window() -> WalkForwardWindow:

    return WalkForwardWindow(
        training_start=datetime(
            2026,
            1,
            1,
            tzinfo=timezone.utc,
        ),
        training_end=datetime(
            2026,
            3,
            1,
            tzinfo=timezone.utc,
        ),
        validation_start=datetime(
            2026,
            3,
            1,
            tzinfo=timezone.utc,
        ),
        validation_end=datetime(
            2026,
            3,
            20,
            tzinfo=timezone.utc,
        ),
    )

def test_configuration() -> None:

    config = WalkForwardConfig(
        training_days=60,
        validation_days=20,
        step_days=20,
    )

    assert config.training_days == 60


def test_window() -> None:

    window = build_window()

    assert window.training_duration_days == 59
    assert window.validation_duration_days == 19


def test_engine_execution() -> None:

    engine = build_engine()

    result = engine.run(
        windows=[build_window()],
    )

    assert isinstance(
        result,
        WalkForwardResult,
    )

    assert result.iteration_count == 1


def test_service_execution() -> None:

    service = WalkForwardService(
        engine=build_engine(),
    )

    result = service.run(
        config=WalkForwardConfig(
            training_days=60,
            validation_days=20,
            step_days=20,
        ),
        windows=[build_window()],
    )

    assert isinstance(
        result,
        WalkForwardResult,
    )

    assert result.iteration_count == 1


def test_determinism() -> None:

    engine = build_engine()

    first = engine.run(
        windows=[build_window()],
    )

    second = engine.run(
        windows=[build_window()],
    )

    assert first == second


def main() -> None:

    test_configuration()
    test_window()
    test_engine_execution()
    test_service_execution()
    test_determinism()

    print("=" * 60)
    print("Walk-Forward Validation Passed")
    print("=" * 60)
    print()
    print("Configuration   : OK")
    print("Window          : OK")
    print("Engine          : OK")
    print("Service         : OK")
    print("Determinism     : OK")
    print()
    print("=" * 60)


if __name__ == "__main__":
    main()