"""
Reporting exporter abstraction.

This module defines the common interface implemented by all report exporters.
Exporters are responsible solely for serializing immutable BacktestReport
instances into presentation formats.

Exporters perform no calculations, no file I/O, and no mutation of the report.
"""

from __future__ import annotations

from typing import Protocol

from app.backtest.reporting.report import BacktestReport


class ReportExporter(Protocol):
    """
    Common protocol implemented by all report exporters.

    Implementations serialize a BacktestReport into a specific presentation
    format such as console text, CSV, or JSON.

    Exporters are expected to be:

    - Stateless
    - Deterministic
    - Side-effect free
    """

    def export(self, report: BacktestReport) -> str:
        """
        Serialize a completed backtest report.

        Parameters
        ----------
        report
            Immutable report to serialize.

        Returns
        -------
        str
            Serialized representation of the supplied report.
        """
        ...