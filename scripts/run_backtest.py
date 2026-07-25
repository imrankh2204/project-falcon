"""
Project Falcon backtest executable entry point.

This module acts only as the execution entry point.

Responsibilities
----------------
- Build runtime configuration.
- Request application creation from factory.
- Execute backtest.
- Generate reports.
- Persist exported reports.

This module intentionally does NOT implement:

- Dependency construction
- Trading logic
- Strategy logic
- Replay logic
- Risk rules
- Performance calculations
"""

from __future__ import annotations

from pathlib import Path

from app.backtest.application_factory import (
    BacktestApplicationFactory,
)
from app.backtest.backtest_config import (
    BacktestConfig,
)
from app.backtest.reporting.console import (
    ConsoleExporter,
)
from app.backtest.reporting.csv import (
    CsvExporter,
)
from app.backtest.reporting.json import (
    JsonExporter,
)
from app.market.instrument import Instrument
from app.market.timeframe import TimeFrame
from app.strategies.ema_parameters import (
    EMACrossoverParameters,
)
from app.strategies.strategy_factory import (
    StrategyFactory,
)


def write_report(
    *,
    output_directory: Path,
    filename: str,
    content: str,
) -> None:
    """
    Persist exported report content.
    """

    output_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    path = output_directory / filename

    path.write_text(
        content,
        encoding="utf-8",
    )


def build_application(
    config: BacktestConfig,
):
    """
    Build a runnable backtest application.

    Application construction is delegated to
    BacktestApplicationFactory.
    """

    parameters = EMACrossoverParameters(
        fast_period=9,
        slow_period=21,
    )

    strategy = StrategyFactory.create(
        parameters,
    )

    factory = BacktestApplicationFactory(
        config,
    )

    return factory.create(
        strategy,
    )


def main() -> int:
    """
    Execute a complete Falcon backtest.
    """

    config = BacktestConfig(
        csv_path=Path(
            "data/historical/sample.csv"
        ),
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
            "data/reports"
        ),
    )

    application = build_application(
        config,
    )

    report = application.run()

    if config.export_console:
        print(
            ConsoleExporter().export(
                report,
            )
        )

    if config.export_csv:
        write_report(
            output_directory=config.output_directory,
            filename="backtest_report.csv",
            content=CsvExporter().export(
                report,
            ),
        )

    if config.export_json:
        write_report(
            output_directory=config.output_directory,
            filename="backtest_report.json",
            content=JsonExporter().export(
                report,
            ),
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )