"""
Project Falcon backtest executable entry point.

This module acts as the Composition Root for backtest execution.

Responsibilities:
    - Build application dependencies.
    - Execute BacktestApplication.
    - Generate reports.
    - Persist exported reports.

This module intentionally does NOT implement:

    - Trading logic
    - Strategy logic
    - Replay logic
    - Risk rules
    - Performance calculations
"""

from __future__ import annotations

from pathlib import Path

from app.backtest.backtest_config import BacktestConfig
from app.backtest.backtest_session import BacktestSession
from app.backtest.csv_provider import CsvHistoricalProvider
from app.backtest.replay_clock import ReplayClock
from app.backtest.replay_engine import ReplayEngine
from app.backtest.reporting.builder import ReportBuilder
from app.backtest.reporting.console import ConsoleExporter
from app.backtest.reporting.csv import CsvExporter
from app.backtest.reporting.json import JsonExporter
from app.core.backtest_application import BacktestApplication
from app.market.instrument import Instrument
from app.market.timeframe import TimeFrame
from app.services.trade_signal_translator import TradeSignalTranslator
from app.strategies.ema_crossover import EMACrossoverStrategy
from app.trading.execution import PaperExecutionEngine
from app.trading.portfolio import Portfolio
from app.trading.risk_manager import RiskManager
from app.trading.trading_service import TradingService


def build_backtest_application(
    config: BacktestConfig,
) -> BacktestApplication:
    """
    Build the complete backtest application dependency graph.

    Parameters
    ----------
    config
        Immutable backtest runtime configuration.

    Returns
    -------
    BacktestApplication
        Fully configured backtest application.
    """

    provider = CsvHistoricalProvider(
        csv_path=config.csv_path,
        timeframe=config.timeframe,
    )

    first_candle = next(
        provider.candles()
    )

    replay_clock = ReplayClock(
        start_time=first_candle.timestamp
    )

    replay_engine = ReplayEngine(
        provider=provider,
        clock=replay_clock,
    )

    strategy = EMACrossoverStrategy(
        fast_period=9,
        slow_period=21,
    )

    risk_manager = RiskManager()

    execution_engine = PaperExecutionEngine()

    portfolio = Portfolio()

    trading_service = TradingService(
        risk_manager=risk_manager,
        execution_engine=execution_engine,
        portfolio=portfolio,
    )

    signal_translator = TradeSignalTranslator()

    session = BacktestSession(
        replay_engine=replay_engine,
        instrument=config.instrument,
        strategy=strategy,
        trading_service=trading_service,
        signal_translator=signal_translator,
        quantity=config.quantity,
    )

    return BacktestApplication(
        session=session,
        report_builder=ReportBuilder(),
    )


def write_report(
    *,
    output_directory: Path,
    filename: str,
    content: str,
) -> None:
    """
    Persist exported report content.

    Parameters
    ----------
    output_directory
        Target directory.

    filename
        Output filename.

    content
        Serialized report content.
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


def main() -> int:
    """
    Execute a complete Falcon backtest.

    Returns
    -------
    int
        Process exit code.
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

    application = build_backtest_application(
        config
    )

    result = application.run()

    report = ReportBuilder().build(
        result
    )

    if config.export_console:
        print(
            ConsoleExporter().export(
                report
            )
        )

    if config.export_csv:
        write_report(
            output_directory=config.output_directory,
            filename="backtest_report.csv",
            content=CsvExporter().export(report),
        )

    if config.export_json:
        write_report(
            output_directory=config.output_directory,
            filename="backtest_report.json",
            content=JsonExporter().export(report),
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )