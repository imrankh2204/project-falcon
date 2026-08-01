"""
Project-Falcon
Live Runtime Lifecycle Manager

FAL-520-R2

Responsibilities:
- Own live runtime lifecycle
- Start and stop LiveEngine
- Coordinate event source lifecycle
- Provide application-level runtime boundary

The LiveRuntime intentionally does NOT:
- process trading logic
- evaluate strategies
- manage positions
- communicate directly with brokers

It is a composition and lifecycle layer only.
"""

from __future__ import annotations

import logging
from typing import Any, Optional


logger = logging.getLogger(__name__)


class LiveRuntime:
    """
    Application runtime coordinator for live trading.

    Architecture:

        LiveRuntime
             |
             |
             v
        LiveEngine
             |
             |
             v
        Trading Pipeline


    Optional Event Source:

        Market Feed
             |
             v
        LiveRuntime
             |
             v
        LiveEngine.process_event()
    """

    def __init__(
        self,
        live_engine: Any,
        event_source: Optional[Any] = None,
    ):
        """
        Initialize LiveRuntime.

        Dependencies are injected to preserve:
        - Clean Architecture
        - Testability
        - Broker independence
        """

        self.live_engine = live_engine
        self.event_source = event_source

        self.running = False

        logger.info(
            "LiveRuntime initialized"
        )

    # ------------------------------------------------------------------
    # Lifecycle Management
    # ------------------------------------------------------------------

    def start(self) -> None:
        """
        Start live runtime.

        Startup order:

        1. Start LiveEngine
        2. Start event source (if available)
        """

        if self.running:
            logger.warning(
                "LiveRuntime already running"
            )
            return

        try:
            self.live_engine.start()

            if self.event_source is not None:
                self.event_source.start()

            self.running = True

            logger.info(
                "LiveRuntime started"
            )

        except Exception:
            logger.exception(
                "LiveRuntime startup failed"
            )

            self.stop()

            raise

    def stop(self) -> None:
        """
        Stop live runtime.

        Shutdown order:

        1. Stop event source
        2. Stop LiveEngine
        """

        if not self.running:
            return

        try:
            if self.event_source is not None:
                self.event_source.stop()

            self.live_engine.stop()

            self.running = False

            logger.info(
                "LiveRuntime stopped"
            )

        except Exception:
            logger.exception(
                "LiveRuntime shutdown failed"
            )

            self.running = False

    # ------------------------------------------------------------------
    # Event Handling
    # ------------------------------------------------------------------

    def process_event(self, event: Any) -> Optional[Any]:
        """
        Forward market events to LiveEngine.

        This method exists as the future callback
        target for live market data providers.
        """

        if not self.running:
            logger.warning(
                "Ignoring event while runtime stopped"
            )

            return None

        return self.live_engine.process_event(event)

    def run(self) -> None:
        """
        Execute the runtime using the configured event source.

        The runtime remains deterministic because the event source
        controls event ordering and pacing.

        Raises
        ------
        RuntimeError
            If no event source has been configured.
        """

        if self.event_source is None:
            raise RuntimeError(
                "LiveRuntime requires an event source."
            )

        if not self.running:
            self.start()

        try:
            for event in self.event_source.events():
                self.process_event(event)

        finally:
            self.stop()