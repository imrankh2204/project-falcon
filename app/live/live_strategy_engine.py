"""
Live strategy engine.

Coordinates execution of Falcon strategies for live events.

Responsibilities
----------------
- Receive LiveEvent objects.
- Build StrategyContext instances.
- Execute the StrategyEngine.
- Return generated signals.

The engine intentionally does NOT implement:

- Market data streaming
- Order execution
- Risk management
- Broker communication
"""

from __future__ import annotations

from app.live.live_event import (
    LiveEvent,
)
from app.live.strategy_context_builder import (
    StrategyContextBuilder,
)
from app.strategies.engine import (
    StrategyEngine,
)
from app.strategies.signal import (
    Signal,
)


class LiveStrategyEngine:
    """
    Executes Falcon strategies for live events.
    """

    def __init__(
        self,
        *,
        strategy_engine: StrategyEngine,
        context_builder: StrategyContextBuilder,
    ) -> None:

        if not isinstance(
            strategy_engine,
            StrategyEngine,
        ):
            raise TypeError(
                "strategy_engine must be a StrategyEngine."
            )

        if not isinstance(
            context_builder,
            StrategyContextBuilder,
        ):
            raise TypeError(
                "context_builder must be a StrategyContextBuilder."
            )

        self._strategy_engine = strategy_engine
        self._context_builder = context_builder

    @property
    def strategy_engine(
        self,
    ) -> StrategyEngine:
        """
        Return the configured strategy engine.
        """

        return self._strategy_engine

    def evaluate(
        self,
        event: LiveEvent,
    ) -> dict[str, Signal]:
        """
        Evaluate all strategies for a live event.
        """

        if not isinstance(
            event,
            LiveEvent,
        ):
            raise TypeError(
                "event must be a LiveEvent."
            )

        context = self._context_builder.build(
            event,
        )

        return self._strategy_engine.evaluate(
            context,
        )