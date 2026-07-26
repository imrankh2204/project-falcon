"""
Validation suite for the complete optimization pipeline.

Verifies:
- Parameter generation.
- Workflow execution.
- Report construction.
- Ranking integration.
- Console export.
- Deterministic behaviour.

This validation intentionally does NOT test:
- Live trading
- Broker integration
- Market data loading
- Strategy calculations
"""

from __future__ import annotations

from datetime import datetime, timezone

from app.backtest.advanced_performance_snapshot import (
    AdvancedPerformanceSnapshot,
)

from app.backtest.equity_curve_snapshot import (
    EquityCurveSnapshot,
)

from app.backtest.optimization.console import (
    OptimizationConsoleExporter,
)

from app.backtest.optimization.parameter_grid import (
    ParameterGrid,
)

from app.backtest.optimization.ranking import (
    RankingEngine,
    RankingMetric,
)

from app.backtest.optimization.report import (
    OptimizationReport,
)

from app.backtest.optimization.result import (
    OptimizationResult,
)

from app.backtest.optimization.workflow import (
    OptimizationWorkflow,
)

from app.backtest.performance_snapshot import (
    PerformanceSnapshot,
)

from app.backtest.reporting.report import (
    BacktestReport,
)

from app.market.instrument import (
    Instrument,
)

from app.strategies.ema_parameters import (
    EMACrossoverParameters,
)


class FakeExecutor:
    """
    Deterministic optimization executor stub.
    """

    def execute(
        self,
        parameters: EMACrossoverParameters,
    ) -> OptimizationResult:

        performance = PerformanceSnapshot(
            trade_count=10,
            winning_trades=6,
            losing_trades=4,
            win_rate=60.0,
            gross_profit=1000.0,
            gross_loss=400.0,
            net_profit=float(
                parameters.fast_period
            ),
            average_win=166.66,
            average_loss=100.0,
            largest_win=300.0,
            largest_loss=150.0,
        )

        advanced_performance = AdvancedPerformanceSnapshot(
            profit_factor=2.5,
            expectancy=60.0,
            sharpe_ratio=1.2,
            sortino_ratio=1.5,
        )

        equity_curve = EquityCurveSnapshot(
            points=(),
            peak_equity=100000.0,
            maximum_drawdown=0.0,
            maximum_drawdown_percentage=0.0,
        )

        report = BacktestReport(
            instrument=Instrument(
                exchange="NSE",
                symbol="NIFTY",
                instrument_token=0,
                lot_size=50,
                tick_size=0.05,
            ),
            strategy_name="EMACrossoverStrategy",
            start_time=datetime(
                2026,
                1,
                1,
                9,
                15,
                tzinfo=timezone.utc,
            ),
            end_time=datetime(
                2026,
                1,
                1,
                10,
                50,
                tzinfo=timezone.utc,
            ),
            performance=performance,
            advanced_performance=advanced_performance,
            equity_curve=equity_curve,
        )

        return OptimizationResult(
            parameters=parameters,
            report=report,
        )


class FakeReportBuilder:
    """
    Deterministic optimization report builder.
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


def test_parameter_generation() -> tuple[
    EMACrossoverParameters,
    ...,
]:

    grid = ParameterGrid(
        fast_periods=(5, 9),
        slow_periods=(20, 21),
    )

    parameters = tuple(grid)

    assert len(parameters) == 4

    assert parameters == grid.parameters

    return parameters


def test_workflow_execution(
    parameters: tuple[
        EMACrossoverParameters,
        ...,
    ],
) -> OptimizationReport:

    workflow = OptimizationWorkflow(
        executor=FakeExecutor(),
        report_builder=FakeReportBuilder(),
    )

    report = workflow.run(
        parameters
    )

    assert isinstance(
        report,
        OptimizationReport,
    )

    assert len(
        report.results
    ) == len(parameters)

    return report


def test_ranking_integration(
    report: OptimizationReport,
) -> None:

    ranked = RankingEngine().rank(
        report,
        RankingMetric.NET_PROFIT,
    )

    assert len(ranked) == len(
        report.results
    )


def test_console_export(
    report: OptimizationReport,
) -> None:
    """
    Validate console export.

    Console exporter consumes OptimizationReport.
    """

    output = OptimizationConsoleExporter().export(
        report
    )

    assert (
        "Project Falcon Optimization Report"
        in output
    )


def test_determinism(
    parameters: tuple[
        EMACrossoverParameters,
        ...,
    ],
) -> None:

    first = test_workflow_execution(
        parameters
    )

    second = test_workflow_execution(
        parameters
    )

    assert first.results == second.results


def main() -> None:

    parameters = test_parameter_generation()

    report = test_workflow_execution(
        parameters
    )

    test_ranking_integration(
        report
    )

    test_console_export(
        report
    )

    test_determinism(
        parameters
    )

    print("=" * 60)
    print(
        "Optimization Pipeline Validation Passed"
    )
    print("=" * 60)
    print("")
    print(
        "Parameter Generation     : OK"
    )
    print(
        "Workflow Execution       : OK"
    )
    print(
        "Report Construction      : OK"
    )
    print(
        "Ranking Integration      : OK"
    )
    print(
        "Console Export           : OK"
    )
    print(
        "Determinism              : OK"
    )
    print("")
    print("=" * 60)


if __name__ == "__main__":
    main()