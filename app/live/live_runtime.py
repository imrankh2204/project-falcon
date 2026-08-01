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
from datetime import datetime
from typing import Any, Optional

from app.live.execution_result import ExecutionResult
from app.live.runtime_event import RuntimeEvent
from app.live.runtime_statistics import RuntimeStatistics


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
        #
        # Runtime statistics.
        #
        self._events_processed = 0
        self._accepted_trades = 0
        self._rejected_trades = 0

        self._started_at: datetime | None = None
        self._finished_at: datetime | None = None
        #
        # Runtime event history.
        #
        self._events: list[RuntimeEvent] = []

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

            self._started_at = datetime.now()
            self._finished_at = None

            self._events_processed = 0
            self._accepted_trades = 0
            self._rejected_trades = 0
            self._events.clear()
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

            self._finished_at = datetime.now()
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
        Forward market events to LiveEngine while collecting
        runtime execution statistics.
        """

        if not self.running:
            logger.warning(
                "Ignoring event while runtime stopped"
            )

            return None

        self._events_processed += 1

        result = self.live_engine.process_event(event)

        if isinstance(result, ExecutionResult):

            if result.accepted:
                self._accepted_trades += 1
            else:
                self._rejected_trades += 1

            self._events.append(
                RuntimeEvent(
                    sequence=self._events_processed,
                    timestamp=datetime.now(),
                    accepted=result.accepted,
                    description=(
                        "Trade accepted"
                        if result.accepted
                        else "Trade rejected"
                    ),
                )
            )

        return result

    def statistics(self) -> RuntimeStatistics:
        """
        Return an immutable snapshot of runtime statistics.
        """

        elapsed = None

        if (
            self._started_at is not None
            and self._finished_at is not None
        ):
            elapsed = (
                self._finished_at
                - self._started_at
            )

        return RuntimeStatistics(
            events_processed=self._events_processed,
            accepted_trades=self._accepted_trades,
            rejected_trades=self._rejected_trades,
            started_at=self._started_at,
            finished_at=self._finished_at,
            elapsed=elapsed,
        )

    def events(self) -> tuple[RuntimeEvent, ...]:
        """
        Return an immutable snapshot of the runtime event history.
        """

        return tuple(self._events)

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