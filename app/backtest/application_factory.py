"""
Backtest application factory for Project Falcon.

This module provides reusable construction of isolated backtest application
instances.

Responsibilities
----------------
- Build backtest execution dependencies.
- Create isolated application instances.
- Connect strategy instances with the backtest pipeline.

The BacktestApplicationFactory intentionally does NOT implement:

- Strategy logic
- Optimization logic
- Ranking logic
- Report exporting
- Performance calculations
"""

from __future__ import annotations

from pathlib import Path

from app.backtest.backtest_config import BacktestConfig
from app.backtest.backtest_session import BacktestSession
from app.backtest.csv_provider import CsvHistoricalProvider
from app.backtest.execution_cost_model import ExecutionCostModel
from app.backtest.execution_price_model import ExecutionPriceModel
from app.backtest.replay_clock import ReplayClock
from app.backtest.replay_engine import ReplayEngine
from app.core.backtest_application import BacktestApplication
from app.market.instrument import Instrument
from app.services.trade_signal_translator import (
    TradeSignalTranslator,
)
from app.strategies.strategy import Strategy
from app.trading.execution import PaperExecutionEngine
from app.trading.portfolio import Portfolio
from app.trading.risk_manager import RiskManager
from app.trading.trading_service import TradingService
from app.backtest.reporting.builder import ReportBuilder

class BacktestApplicationFactory:
    """
    Creates isolated BacktestApplication instances.

    Each invocation creates a fresh execution environment:

    - ReplayEngine
    - TradingService
    - Portfolio
    - ExecutionEngine
    - BacktestSession
    """

    def __init__(
        self,
        config: BacktestConfig,
    ) -> None:

        if not isinstance(
            config,
            BacktestConfig,
        ):
            raise TypeError(
                "config must be a BacktestConfig."
            )

        self._config = config

    @property
    def config(self) -> BacktestConfig:
        """
        Return immutable backtest configuration.
        """

        return self._config

    def create(
        self,
        strategy: Strategy,
    ) -> BacktestApplication:
        """
        Create an isolated backtest application.

        Parameters
        ----------
        strategy
            Strategy instance to evaluate.

        Returns
        -------
        BacktestApplication
            Fresh executable backtest application.
        """

        if not isinstance(
            strategy,
            Strategy,
        ):
            raise TypeError(
                "strategy must be a Strategy."
            )

        provider = CsvHistoricalProvider(
            csv_path=self._config.csv_path,
            timeframe=self._config.timeframe,
            date_range=self._config.date_range,
        )

        try:
            first_candle = next(
                provider.candles()
            )
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

        risk_manager = RiskManager()

        execution_engine = PaperExecutionEngine()

        portfolio = Portfolio()

        trading_service = TradingService(
            risk_manager=risk_manager,
            execution_engine=execution_engine,
            portfolio=portfolio,
        )

        signal_translator = (
            TradeSignalTranslator()
        )

        execution_price_model = (
            ExecutionPriceModel(
                slippage_per_unit=0.05,
            )
        )

        execution_cost_model = (
            ExecutionCostModel(
                commission_rate=0.0,
                slippage_per_unit=0.05,
            )
        )

        session = BacktestSession(
            replay_engine=replay_engine,
            instrument=self._config.instrument,
            strategy=strategy,
            trading_service=trading_service,
            signal_translator=signal_translator,
            execution_price_model=execution_price_model,
            execution_cost_model=execution_cost_model,
            quantity=self._config.quantity,
        )

        report_builder = ReportBuilder()
        
        return BacktestApplication(
            session=session,
            report_builder=report_builder,
        )