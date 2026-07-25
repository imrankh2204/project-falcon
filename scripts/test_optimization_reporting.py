"""
Optimization reporting validation for Project Falcon.

Validates:
    - Optimization report construction
    - Ranking behaviour
    - Console export
    - Deterministic ordering

This validation follows the current immutable reporting contracts.
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
from app.backtest.performance_snapshot import (
    PerformanceSnapshot,
)
from app.backtest.reporting.report import (
    BacktestReport,
)
from app.market.instrument import Instrument
from app.strategies.ema_parameters import (
    EMACrossoverParameters,
)


def _performance(
    profit: float,
    win_rate: float,
) -> PerformanceSnapshot:
    """
    Create deterministic performance snapshot.
    """

    return PerformanceSnapshot(
        trade_count=10,
        winning_trades=6,
        losing_trades=4,
        win_rate=win_rate,
        gross_profit=profit,
        gross_loss=100.0,
        net_profit=profit - 100.0,
        average_win=profit / 6,
        average_loss=25.0,
        largest_win=profit / 2,
        largest_loss=50.0,
    )


def _advanced_performance(
    factor: float,
) -> AdvancedPerformanceSnapshot:
    """
    Create deterministic advanced metrics snapshot.
    """

    return AdvancedPerformanceSnapshot(
        profit_factor=factor,
        expectancy=100.0,
        sharpe_ratio=1.2,
        sortino_ratio=1.5,
    )


def _equity_curve() -> EquityCurveSnapshot:
    """
    Create deterministic equity curve snapshot.
    """

    return EquityCurveSnapshot(
        points=(),
        peak_equity=100000.0,
        maximum_drawdown=500.0,
        maximum_drawdown_percentage=0.5,
    )


def _result(
    name: str,
    profit: float,
    win_rate: float,
    factor: float,
) -> OptimizationResult:
    """
    Build complete optimization result.
    """

    parameters = EMACrossoverParameters(
        fast_period=9,
        slow_period=21,
    )

    report = BacktestReport(
        instrument=Instrument(
            exchange="NSE",
            symbol="NIFTY",
            instrument_token=1,
            lot_size=50,
            tick_size=0.05,
        ),
        strategy_name=name,
        start_time=datetime(
            2026,
            1,
            1,
            tzinfo=timezone.utc,
        ),
        end_time=datetime(
            2026,
            1,
            2,
            tzinfo=timezone.utc,
        ),
        performance=_performance(
            profit,
            win_rate,
        ),
        advanced_performance=_advanced_performance(
            factor,
        ),
        equity_curve=_equity_curve(),
    )

    return OptimizationResult(
        parameters=parameters,
        report=report,
    )


def test_report_construction() -> None:
    """
    Validate optimization report construction.
    """

    report = OptimizationReport(
        results=(
            _result(
                "EMA-A",
                1000.0,
                60.0,
                1.5,
            ),
        )
    )

    assert len(report.results) == 1


def test_profit_ranking() -> None:
    """
    Validate ranking by net profit.
    """

    report = OptimizationReport(
        results=(
            _result(
                "EMA-A",
                1000.0,
                60.0,
                1.5,
            ),
            _result(
                "EMA-B",
                2000.0,
                50.0,
                1.2,
            ),
        )
    )

    ranked = RankingEngine().rank(
        report,
        RankingMetric.NET_PROFIT,
    )

    assert (
        ranked[0]
        .report
        .performance
        .net_profit
        >
        ranked[1]
        .report
        .performance
        .net_profit
    )


def test_win_rate_ranking() -> None:
    """
    Validate ranking by win rate.
    """

    report = OptimizationReport(
        results=(
            _result(
                "EMA-A",
                1000.0,
                40.0,
                1.5,
            ),
            _result(
                "EMA-B",
                900.0,
                80.0,
                1.2,
            ),
        )
    )

    ranked = RankingEngine().rank(
        report,
        RankingMetric.WIN_RATE,
    )

    assert (
        ranked[0]
        .report
        .performance
        .win_rate
        ==
        80.0
    )


def test_profit_factor_ranking() -> None:
    """
    Validate ranking by advanced profit factor.
    """

    report = OptimizationReport(
        results=(
            _result(
                "EMA-A",
                1000.0,
                60.0,
                1.5,
            ),
            _result(
                "EMA-B",
                1200.0,
                60.0,
                2.0,
            ),
        )
    )

    ranked = RankingEngine().rank(
        report,
        RankingMetric.PROFIT_FACTOR,
    )

    assert (
        ranked[0]
        .report
        .advanced_performance
        .profit_factor
        ==
        2.0
    )


def test_console_export() -> None:
    """
    Validate console reporting.
    """

    report = OptimizationReport(
        results=(
            _result(
                "EMA",
                1000.0,
                60.0,
                1.5,
            ),
        )
    )

    output = OptimizationConsoleExporter().export(
        report
    )

    assert "EMA" in output


def test_determinism() -> None:
    """
    Validate deterministic ranking.
    """

    report = OptimizationReport(
        results=(
            _result(
                "EMA-A",
                1000.0,
                60.0,
                1.5,
            ),
            _result(
                "EMA-B",
                2000.0,
                70.0,
                1.8,
            ),
        )
    )

    engine = RankingEngine()

    first = engine.rank(
        report,
        RankingMetric.NET_PROFIT,
    )

    second = engine.rank(
        report,
        RankingMetric.NET_PROFIT,
    )

    assert first == second


def main() -> None:

    test_report_construction()
    test_profit_ranking()
    test_win_rate_ranking()
    test_profit_factor_ranking()
    test_console_export()
    test_determinism()

    print("=" * 60)
    print("Optimization Reporting Validation Passed")
    print("=" * 60)
    print()
    print("Report Construction : OK")
    print("Profit Ranking      : OK")
    print("Win Rate Ranking    : OK")
    print("Profit Factor       : OK")
    print("Console Export      : OK")
    print("Determinism         : OK")
    print()
    print("=" * 60)


if __name__ == "__main__":
    main()