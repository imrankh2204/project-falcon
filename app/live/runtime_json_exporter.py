"""
Project Falcon

FAL-580-R1

Runtime JSON Exporter

Exports immutable RuntimeSessionReport objects to JSON.
"""

from __future__ import annotations

import json
from pathlib import Path

from app.live.runtime_session_report import (
    RuntimeSessionReport,
)


class RuntimeJsonExporter:
    """
    Exports runtime session reports to JSON.
    """

    def export(
        self,
        report: RuntimeSessionReport,
        output_file: str | Path,
    ) -> None:
        """
        Export a runtime session report to JSON.
        """

        if not isinstance(
            report,
            RuntimeSessionReport,
        ):
            raise TypeError(
                "report must be a RuntimeSessionReport."
            )

        output_path = Path(output_file)

        payload = {
            "statistics": {
                "events_processed": (
                    report.statistics.events_processed
                ),
                "accepted_trades": (
                    report.statistics.accepted_trades
                ),
                "rejected_trades": (
                    report.statistics.rejected_trades
                ),
                "started_at": (
                    report.statistics.started_at.isoformat()
                    if report.statistics.started_at
                    else None
                ),
                "finished_at": (
                    report.statistics.finished_at.isoformat()
                    if report.statistics.finished_at
                    else None
                ),
                "elapsed": (
                    str(report.statistics.elapsed)
                    if report.statistics.elapsed
                    else None
                ),
            },
            "events": [
                {
                    "sequence": event.sequence,
                    "timestamp": (
                        event.timestamp.isoformat()
                    ),
                    "accepted": event.accepted,
                }
                for event in report.events
            ],
        }

        output_path.write_text(
            json.dumps(
                payload,
                indent=4,
            ),
            encoding="utf-8",
        )