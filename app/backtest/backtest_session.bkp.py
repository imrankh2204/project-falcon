"""
Backtest session for Project Falcon.

Coordinates execution of a historical replay session.

Responsibilities:
    - Own the replay session lifecycle.
    - Validate replay infrastructure.
    - Execute the replay until completion.

The BacktestSession intentionally does NOT implement:

    - Strategy evaluation
    - Order execution
    - Portfolio management
    - Risk management
    - Performance reporting
    - Exception handling beyond fail-fast validation
"""

from __future__ import annotations

from app.backtest.replay_engine import ReplayEngine


class BacktestSession:
    """
    Application service coordinating a historical replay session.

    A BacktestSession owns a ReplayEngine and is responsible for
    executing the replay lifecycle. During FAL-140 the session
    consumes replay events without performing any business logic.
    Future milestones will integrate strategy evaluation and
    execution into the replay loop.
    """

    def __init__(
        self,
        replay_engine: ReplayEngine,
    ) -> None:
        """
        Initialize the backtest session.

        Parameters
        ----------
        replay_engine:
            Replay engine used to execute the historical replay.

        Raises
        ------
        TypeError
            If replay_engine is not a ReplayEngine.
        """

        if not isinstance(replay_engine, ReplayEngine):
            raise TypeError(
                "replay_engine must be a ReplayEngine."
            )

        self._replay_engine = replay_engine

    @property
    def replay_engine(self) -> ReplayEngine:
        """
        Return the replay engine owned by this session.
        """
        return self._replay_engine

    def run(self) -> None:
        """
        Execute the replay session.

        The replay engine is iterated until completion. Replay events
        are intentionally consumed without further processing during
        this milestone.

        Empty replay datasets are treated as successful execution.

        Raises
        ------
        Exception
            Any exception raised by the replay engine is propagated
            unchanged.
        """

        for _ in self._replay_engine.replay():
            pass