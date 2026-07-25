"""
Backtest session for Project Falcon.

Coordinates deterministic historical replay with strategy evaluation
and trading lifecycle execution.

Responsibilities:
    - Own replay session lifecycle.
    - Build StrategyContext snapshots.
    - Evaluate strategies.
    - Translate trading signals into TradeRequests.
    - Model execution prices.
    - Delegate trade execution to TradingService.
    - Coordinate position exits.
    - Produce performance analytics.

The BacktestSession intentionally does NOT implement:

    - Risk management
    - Order execution
    - Portfolio accounting
    - Position lifecycle rules
    - Performance calculations
"""

from __future__ import annotations

from app.backtest.advanced_metrics import (
    AdvancedPerformanceMetrics,
)
from app.backtest.advanced_performance_snapshot import (
    AdvancedPerformanceSnapshot,
)
from app.backtest.backtest_result import BacktestResult
from app.backtest.equity_curve import EquityCurve
from app.backtest.equity_curve_snapshot import (
    EquityCurveSnapshot,
)
from app.backtest.execution_cost_model import ExecutionCostModel
from app.backtest.execution_price_model import ExecutionPriceModel
from app.backtest.performance_metrics import PerformanceMetrics
from app.backtest.performance_snapshot import PerformanceSnapshot
from app.backtest.replay_engine import ReplayEngine
from app.market.candle import Candle
from app.market.instrument import Instrument
from app.services.trade_signal_translator import TradeSignalTranslator
from app.strategies.context import StrategyContext
from app.strategies.signal import Signal
from app.strategies.strategy import Strategy
from app.trading.trading_service import TradingService


class BacktestSession:
    """
    Application service coordinating deterministic backtesting.
    """

    def __init__(
        self,
        replay_engine: ReplayEngine,
        instrument: Instrument,
        strategy: Strategy,
        trading_service: TradingService,
        signal_translator: TradeSignalTranslator,
        execution_price_model: ExecutionPriceModel,
        execution_cost_model: ExecutionCostModel,
        quantity: int,
    ) -> None:

        if not isinstance(replay_engine, ReplayEngine):
            raise TypeError(
                "replay_engine must be a ReplayEngine."
            )

        if not isinstance(instrument, Instrument):
            raise TypeError(
                "instrument must be an Instrument."
            )

        if not isinstance(strategy, Strategy):
            raise TypeError(
                "strategy must be a Strategy."
            )

        if not isinstance(trading_service, TradingService):
            raise TypeError(
                "trading_service must be a TradingService."
            )

        if not isinstance(
            signal_translator,
            TradeSignalTranslator,
        ):
            raise TypeError(
                "signal_translator must be a TradeSignalTranslator."
            )

        if not isinstance(
            execution_price_model,
            ExecutionPriceModel,
        ):
            raise TypeError(
                "execution_price_model must be an ExecutionPriceModel."
            )

        if not isinstance(
            execution_cost_model,
            ExecutionCostModel,
        ):
            raise TypeError(
                "execution_cost_model must be an ExecutionCostModel."
            )

        if quantity <= 0:
            raise ValueError(
                "quantity must be greater than zero."
            )

        self._replay_engine = replay_engine
        self._instrument = instrument
        self._strategy = strategy
        self._trading_service = trading_service
        self._signal_translator = signal_translator
        self._execution_price_model = execution_price_model
        self._execution_cost_model = execution_cost_model
        self._quantity = quantity

    def run(self) -> BacktestResult:

        history: list[Candle] = []

        first_candle: Candle | None = None
        last_candle: Candle | None = None

        trades_today = 0

        for replay_event in self._replay_engine.replay():

            candle = replay_event.candle

            if first_candle is None:
                first_candle = candle

            last_candle = candle

            history.append(candle)

            context = self._build_context(history)

            signal = self._strategy.evaluate(context)

            self._handle_signal(
                signal=signal,
                candle=candle,
                trades_today=trades_today,
            )

            if signal == Signal.BUY:
                trades_today += 1

        if last_candle is not None:
            self._trading_service.close_all_open_positions(
                exit_price=last_candle.close,
                exit_time=last_candle.timestamp,
            )

        return self._build_result(
            first_candle=first_candle,
            last_candle=last_candle,
        )

    def _handle_signal(
        self,
        *,
        signal: Signal,
        candle: Candle,
        trades_today: int,
    ) -> None:

        if signal == Signal.HOLD:
            return

        if signal == Signal.BUY:

            trade_request = self._signal_translator.translate(
                instrument=self._instrument,
                signal=signal,
                quantity=self._quantity,
            )

            execution_price = (
                self._execution_price_model.buy_price(
                    candle.close
                )
            )

            self._trading_service.submit_trade(
                trade_request,
                execution_price=execution_price,
                trades_today=trades_today,
            )

            return

        if signal == Signal.SELL:

            exit_price = (
                self._execution_price_model.sell_price(
                    candle.close
                )
            )

            self._trading_service.close_open_position(
                instrument=self._instrument,
                exit_price=exit_price,
                exit_time=candle.timestamp,
            )
            
            return
            
            raise ValueError(
                f"Unsupported signal: {signal}"
            )

    def _build_context(
        self,
        candles: list[Candle],
    ) -> StrategyContext:

        return StrategyContext(
            instrument=self._instrument,
            timeframe=candles[-1].timeframe,
            candles=list(candles),
        )

    def _build_result(
        self,
        *,
        first_candle: Candle | None,
        last_candle: Candle | None,
    ) -> BacktestResult:

        closed_positions = (
            self._trading_service
            .portfolio
            .get_closed_positions()
        )

        performance: PerformanceSnapshot = (
            PerformanceMetrics.calculate(
                closed_positions,
                execution_cost_model=(
                    self._execution_cost_model
                ),
            )
        )

        advanced_performance: (
            AdvancedPerformanceSnapshot
        ) = AdvancedPerformanceMetrics.calculate(
            closed_positions,
        )

        equity_curve: EquityCurveSnapshot = (
            EquityCurve.calculate(
                closed_positions,
            )
        )

        return BacktestResult(
            instrument=self._instrument,
            strategy_name=self._strategy.__class__.__name__,
            start_time=(
                first_candle.timestamp
                if first_candle
                else None
            ),
            end_time=(
                last_candle.timestamp
                if last_candle
                else None
            ),
            performance=performance,
            advanced_performance=advanced_performance,
            equity_curve=equity_curve,
        )