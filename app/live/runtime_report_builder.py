"""
Project Falcon

FAL-570-R2

Runtime Report Builder

Builds immutable RuntimeSessionReport objects from a completed
LiveRuntime.
"""

from __future__ import annotations

from app.live.live_runtime import LiveRuntime
from app.live.runtime_session_report import (
    RuntimeSessionReport,
)


class RuntimeReportBuilder:
    """
    Builds immutable runtime session reports.
    """

    def build(
        self,
        runtime: LiveRuntime,
    ) -> RuntimeSessionReport:
        """
        Build a RuntimeSessionReport from a LiveRuntime.
        """

        if not isinstance(
            runtime,
            LiveRuntime,
        ):
            raise TypeError(
                "runtime must be a LiveRuntime."
            )

        return RuntimeSessionReport(
            statistics=runtime.statistics(),
            events=runtime.events(),
        )