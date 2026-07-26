"""
Validation suite for optimization export.

Verifies:
- CSV serialization.
- JSON serialization.
- File persistence.
- Deterministic output.

This validation intentionally does NOT test:
- Optimization execution
- Strategy logic
- Ranking
- CLI integration
"""

from __future__ import annotations

from pathlib import Path
import tempfile

from app.backtest.advanced_performance_snapshot import (
    AdvancedPerformanceSnapshot,
)
from app.backtest.equity_curve_snapshot import (
    EquityCurveSnapshot,
)
from app.backtest.optimization.csv import (
    OptimizationCsvExporter,
)
from app.backtest.optimization.exporter import (
    OptimizationExporter,
)
from app.backtest.optimization.json import (
    OptimizationJsonExporter,
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


def build_report() -> OptimizationReport:

    performance = PerformanceSnapshot(
        trade_count=10,
        winning_trades=6,
        losing_trades=4,
        win_rate=60.0,
        gross_profit=1000.0,
        gross_loss=400.0,
        net_profit=600.0,
        average_win=166.67,
        average_loss=100.0,
        largest_win=300.0,
        largest_loss=150.0,
    )

    advanced = AdvancedPerformanceSnapshot(
        profit_factor=2.5,
        expectancy=60.0,
        sharpe_ratio=1.2,
        sortino_ratio=1.5,
    )

    equity = EquityCurveSnapshot(
        points=(),
        peak_equity=100000.0,
        maximum_drawdown=0.0,
        maximum_drawdown_percentage=0.0,
    )

    backtest = BacktestReport(
        instrument=Instrument(
            exchange="NSE",
            symbol="NIFTY",
            instrument_token=0,
            lot_size=50,
            tick_size=0.05,
        ),
        strategy_name="EMA",
        start_time=None,
        end_time=None,
        performance=performance,
        advanced_performance=advanced,
        equity_curve=equity,
    )

    result = OptimizationResult(
        parameters=EMACrossoverParameters(
            fast_period=9,
            slow_period=21,
        ),
        report=backtest,
    )

    return OptimizationReport(
        results=(result,),
    )


def test_csv_export() -> None:

    report = build_report()

    output = OptimizationCsvExporter().export(
        report
    )

    assert "fast_period" in output
    assert "9" in output
    assert "21" in output


def test_json_export() -> None:

    report = build_report()

    output = OptimizationJsonExporter().export(
        report
    )

    assert "fast_period" in output
    assert "profit_factor" in output


def test_file_export() -> None:

    report = build_report()

    csv_text = (
        OptimizationCsvExporter().export(
            report
        )
    )

    with tempfile.TemporaryDirectory() as directory:

        path = (
            Path(directory)
            / "optimization.csv"
        )

        OptimizationExporter().write(
            output_path=path,
            content=csv_text,
        )

        assert path.exists()

        assert (
            path.read_text(
                encoding="utf-8"
            )
            == csv_text
        )


def test_determinism() -> None:

    report = build_report()

    csv_exporter = (
        OptimizationCsvExporter()
    )

    json_exporter = (
        OptimizationJsonExporter()
    )

    assert (
        csv_exporter.export(report)
        ==
        csv_exporter.export(report)
    )

    assert (
        json_exporter.export(report)
        ==
        json_exporter.export(report)
    )


def main() -> None:

    test_csv_export()
    test_json_export()
    test_file_export()
    test_determinism()

    print("=" * 60)
    print(
        "Optimization Export Validation Passed"
    )
    print("=" * 60)
    print()
    print("CSV Export        : OK")
    print("JSON Export       : OK")
    print("File Persistence  : OK")
    print("Determinism       : OK")
    print()
    print("=" * 60)


if __name__ == "__main__":
    main()