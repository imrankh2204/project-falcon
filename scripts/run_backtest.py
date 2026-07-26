"""
Project Falcon backtest executable entry point.

This module acts as the Composition Root for backtest execution.

Responsibilities
----------------
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
from app.backtest.execution_price_model import ExecutionPriceModel
from app.backtest.replay_clock import ReplayClock
from app.backtest.replay_engine import ReplayEngine
from app.backtest.reporting.builder import ReportBuilder
from app.backtest.reporting.console import ConsoleExporter
from app.backtest.reporting.csv import CsvExporter
from app.backtest.reporting.json import JsonExporter
from app.core.backtest_application import BacktestApplication
from app.market.instrument import Instrument
from app.market.timeframe import TimeFrame
from app.services.trade_signal_translator import (
    TradeSignalTranslator,
)
from app.strategies.ema_parameters import (
    EMACrossoverParameters,
)
from app.strategies.strategy_factory import (
    StrategyFactory,
)
from app.trading.execution import PaperExecutionEngine
from app.trading.portfolio import Portfolio
from app.trading.risk_manager import RiskManager
from app.trading.trading_service import TradingService
from app.backtest.execution_cost_model import (
    ExecutionCostModel,
)

def build_backtest_application(
    config: BacktestConfig,
) -> BacktestApplication:
    """
    Build the complete backtest dependency graph.
    """

    provider = CsvHistoricalProvider(
        csv_path=config.csv_path,
        timeframe=config.timeframe,
    )

    try:
        first_candle = next(provider.candles())
    except StopIteration as exc:
        raise ValueError(
            "Historical dataset is empty."
        ) from exc

    replay_clock = ReplayClock(
        start_time=first_candle.timestamp,
    )

    replay_engine = ReplayEngine(
        provider=provider,
        clock=replay_clock,
    )

    parameters = EMACrossoverParameters(
        fast_period=9,
        slow_period=21,
    )

    strategy = StrategyFactory.create(
        parameters,
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

    execution_price_model = ExecutionPriceModel(
        slippage_per_unit=0.05,
    )
    
    execution_cost_model = ExecutionCostModel(
        commission_rate=0.0003,
        slippage_per_unit=0.05,
    )

    session = BacktestSession(
        replay_engine=replay_engine,
        instrument=config.instrument,
        strategy=strategy,
        trading_service=trading_service,
        signal_translator=signal_translator,
        execution_price_model=execution_price_model,
        execution_cost_model=execution_cost_model,
        quantity=config.quantity,
    )

    report_builder = ReportBuilder()

    return BacktestApplication(
        session=session,
        report_builder=report_builder,
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

    application = build_backtest_application(
        config
    )

    report = application.run()

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