"""
Project Falcon

FAL-530-R2

Paper Runtime Factory

Creates a fully configured paper trading runtime while preserving
Clean Architecture and broker independence.

Responsibilities
----------------
- Construct PaperBrokerGateway.
- Authenticate the paper broker session.
- Wire live trading services.
- Create the LiveRuntime composition root.

The factory intentionally does NOT:

- Execute trading logic.
- Process market events.
- Evaluate strategies.
- Persist application state.
"""

from __future__ import annotations

from typing import Any

from app.live.live_engine import LiveEngine
from app.live.live_execution_engine import (
    LiveExecutionEngine,
)
from app.live.live_runtime import LiveRuntime
from app.live.live_trading_service import (
    LiveTradingService,
)
from app.paper.paper_broker_gateway import (
    PaperBrokerGateway,
)
from app.portfolio.synchronization_service import (
    PortfolioSynchronizationService,
)


class PaperRuntimeFactory:
    """
    Factory responsible for constructing a fully configured
    paper-trading runtime.
    """

    def create(
        self,
        *,
        strategy_engine: Any,
        signal_translator: Any,
        risk_manager: Any,
        event_source: Any | None = None,
    ) -> LiveRuntime:
        """
        Create and return a configured LiveRuntime
        backed by a PaperBrokerGateway.
        """

        #
        # Paper broker.
        #
        broker_gateway = PaperBrokerGateway()
        broker_gateway.authenticate()

        #
        # Portfolio synchronization.
        #
        synchronization_service = (
            PortfolioSynchronizationService(
                broker_gateway=broker_gateway,
            )
        )

        #
        # Live trading service.
        #
        live_trading_service = LiveTradingService(
            broker_gateway=broker_gateway,
            risk_manager=risk_manager,
            synchronization_service=(
                synchronization_service
            ),
        )

        #
        # Live execution engine.
        #
        live_execution_engine = (
            LiveExecutionEngine(
                live_trading_service=(
                    live_trading_service
                ),
            )
        )

        #
        # Runtime engine.
        #
        live_engine = LiveEngine(
            strategy_engine=strategy_engine,
            trading_service=live_execution_engine,
            signal_translator=signal_translator,
            risk_manager=risk_manager,
        )

        #
        # Application runtime.
        #
        runtime = LiveRuntime(
            live_engine=live_engine,
            event_source=event_source,
        )

        return runtime