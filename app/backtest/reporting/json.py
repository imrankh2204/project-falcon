"""
JSON report exporter.

This module provides JsonExporter, responsible for serializing immutable
BacktestReport instances into JSON format.

The exporter performs serialization only. It contains no business logic,
calculations, persistence, or side effects.
"""

from __future__ import annotations

import json
from dataclasses import asdict

from app.backtest.reporting.exporter import ReportExporter
from app.backtest.reporting.report import BacktestReport


class JsonExporter(ReportExporter):
    """
    Serializes a BacktestReport into JSON.

    The exporter is deterministic and preserves numeric values as JSON
    numbers. Datetime values are emitted using ISO-8601 format.
    """

    def export(self, report: BacktestReport) -> str:
        """
        Serialize a report into JSON.

        Parameters
        ----------
        report
            Immutable report to serialize.

        Returns
        -------
        str
            JSON representation of the supplied report.
        """

        payload = asdict(report)

        payload["start_time"] = report.start_time.isoformat()
        payload["end_time"] = report.end_time.isoformat()

        payload["instrument"] = {
            "exchange": report.instrument.exchange,
            "symbol": report.instrument.symbol,
            "instrument_token": report.instrument.instrument_token,
            "lot_size": report.instrument.lot_size,
            "tick_size": report.instrument.tick_size,
            "expiry": (
                report.instrument.expiry.isoformat()
                if report.instrument.expiry is not None
                else None
            ),
            "strike": report.instrument.strike,
            "option_type": (
                report.instrument.option_type.value
                if report.instrument.option_type is not None
                else None
            ),
        }

        return json.dumps(
            payload,
            indent=4,
            sort_keys=False,
        )