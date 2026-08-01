"""
Strategy context builder for live trading.

Builds immutable StrategyContext objects from incoming live events.

Responsibilities
----------------
- Translate LiveEvent into StrategyContext.
- Keep live pipeline independent from strategy internals.
- Produce immutable strategy contexts.

The builder intentionally does NOT implement:

- Strategy execution
- Signal generation
- Market data streaming
- Trade execution
"""

from __future__ import annotations

from app.live.live_event import (
    LiveEvent,
)
from app.strategies.context import (
    StrategyContext,
)


class StrategyContextBuilder:
    """
    Builds StrategyContext instances from LiveEvent objects.
    """

    def build(
        self,
        event: LiveEvent,
    ) -> StrategyContext:
        """
        Build a StrategyContext from a live event.
        """

        if not isinstance(
            event,
            LiveEvent,
        ):
            raise TypeError(
                "event must be a LiveEvent."
            )

        #
        # Context construction will be expanded in
        # subsequent milestones.
        #
        return StrategyContext(
            market_data=event.tick,
        )