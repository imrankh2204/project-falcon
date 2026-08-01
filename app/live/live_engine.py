"""
Project-Falcon
Live Trading Runtime Engine

FAL-520-R1

Responsibilities:
- Coordinate live event processing
- Connect market events to strategy evaluation
- Translate signals into trade requests
- Apply risk validation
- Submit approved trades

The LiveEngine intentionally does NOT:
- contain strategy logic
- manage broker connections
- manage portfolio state
- persist trades

It is an orchestration layer only.
"""

from __future__ import annotations

import logging
from typing import Any, Optional


logger = logging.getLogger(__name__)


class LiveEngine:
    """
    Event-driven runtime coordinator for live trading.

    Pipeline:

    Market Event
          |
          v
    LiveEngine
          |
          v
    Strategy Engine
          |
          v
    Signal Translator
          |
          v
    Risk Manager
          |
          v
    Trading Service
    """

    def __init__(
        self,
        strategy_engine: Any,
        trading_service: Any,
        signal_translator: Any,
        risk_manager: Any,
    ):
        """
        Initialize LiveEngine dependencies.

        Dependencies are injected to preserve:
        - Clean Architecture
        - Testability
        - Broker independence
        """

        self.strategy_engine = strategy_engine
        self.trading_service = trading_service
        self.signal_translator = signal_translator
        self.risk_manager = risk_manager

        self.running = False

        logger.info("LiveEngine initialized")

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def start(self) -> None:
        """
        Start live runtime.

        Actual event source wiring will be introduced in FAL-520-R2.
        """

        self.running = True

        logger.info("LiveEngine started")

    def stop(self) -> None:
        """
        Stop live runtime.
        """

        self.running = False

        logger.info("LiveEngine stopped")

    # ------------------------------------------------------------------
    # Event Processing
    # ------------------------------------------------------------------

    def process_event(self, event: Any) -> Optional[Any]:
        """
        Process a single market event.

        Flow:

        Event
          |
          v
        Strategy Evaluation
          |
          v
        Signal Translation
          |
          v
        Risk Validation
          |
          v
        Trade Submission

        Returns:
            Execution result if trade submitted.
            None otherwise.
        """

        if not self.running:
            logger.warning(
                "LiveEngine received event while stopped"
            )
            return None

        try:
            logger.debug(
                "Processing market event: %s",
                event,
            )

            signals = self.strategy_engine.evaluate(event)

            if not signals:
                logger.debug(
                    "No strategy signals generated"
                )
                return None

            execution_result = None

            for instrument, signal in signals.items():

                if signal is None:
                    continue

                logger.debug(
                    "Signal generated: %s -> %s",
                    instrument,
                    signal,
                )

                trade_request = (
                    self.signal_translator.translate(
                        instrument=instrument,
                        signal=signal,
                    )
                )

                if trade_request is None:
                    logger.debug(
                        "Signal ignored by translator"
                    )
                    continue

                allowed = self.risk_manager.approve(
                    trade_request,
                    open_positions=[],
                    trades_today=0,
                )

                if not allowed:
                    logger.info(
                        "Trade rejected by risk manager: %s",
                        trade_request,
                    )
                    continue

                execution_result = (
                    self.trading_service.execute(
                        trade_request
                    )
                )

                logger.info(
                    "Trade submitted successfully"
                )

            return execution_result

        except Exception:
            logger.exception(
                "LiveEngine failed processing event"
            )

            return None