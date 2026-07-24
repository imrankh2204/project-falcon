"""
Backtest application facade for Project Falcon.

Coordinates execution of a fully configured BacktestSession and
transforms the resulting BacktestResult into an immutable
BacktestReport.

Responsibilities
----------------
- Execute a configured backtest session.
- Build a reporting model.
- Return an immutable BacktestReport.

The BacktestApplication intentionally does NOT implement:

- Replay orchestration
- Strategy evaluation
- Trade execution
- Performance calculation
- Report exporting
- Dependency construction
"""

from __future__ import annotations

from app.backtest.backtest_session import BacktestSession
from app.backtest.reporting.builder import ReportBuilder
from app.backtest.reporting.report import BacktestReport


class BacktestApplication:
    """
    Application facade for executing a configured backtest.

    This class is intentionally lightweight. All domain and
    application services are composed externally and injected
    through the constructor.
    """

    def __init__(
        self,
        session: BacktestSession,
        report_builder: ReportBuilder,
    ) -> None:
        """
        Initialize the backtest application.

        Parameters
        ----------
        session
            Fully configured backtest session.

        report_builder
            Builder responsible for transforming a BacktestResult
            into a BacktestReport.

        Raises
        ------
        TypeError
            If dependencies are invalid.
        """

        if not isinstance(session, BacktestSession):
            raise TypeError(
                "session must be a BacktestSession."
            )

        if not isinstance(report_builder, ReportBuilder):
            raise TypeError(
                "report_builder must be a ReportBuilder."
            )

        self._session = session
        self._report_builder = report_builder

    @property
    def session(self) -> BacktestSession:
        """
        Return the configured backtest session.
        """

        return self._session

    @property
    def report_builder(self) -> ReportBuilder:
        """
        Return the configured report builder.
        """

        return self._report_builder

    def run(self) -> BacktestReport:
        """
        Execute the configured backtest.

        Workflow
        --------
        1. Execute BacktestSession.
        2. Produce BacktestResult.
        3. Transform result into BacktestReport.
        4. Return immutable report.

        Returns
        -------
        BacktestReport
            Immutable report representing the completed
            backtest execution.
        """

        result = self._session.run()

        return self._report_builder.build(result)