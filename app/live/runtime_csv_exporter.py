"""
Project Falcon

FAL-580-R2

Runtime CSV Exporter

Exports immutable RuntimeSessionReport objects to CSV.
"""

from __future__ import annotations

import csv
from pathlib import Path

from app.live.runtime_session_report import (
    RuntimeSessionReport,
)


class RuntimeCsvExporter:
    """
    Exports runtime session reports to CSV.
    """

    def export(
        self,
        report: RuntimeSessionReport,
        output_directory: str | Path,
    ) -> None:
        """
        Export runtime statistics and events to CSV files.
        """

        if not isinstance(
            report,
            RuntimeSessionReport,
        ):
            raise TypeError(
                "report must be a RuntimeSessionReport."
            )

        output_directory = Path(output_directory)
        output_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        #
        # Statistics
        #
        statistics_file = (
            output_directory
            / "runtime_statistics.csv"
        )

        with statistics_file.open(
            "w",
            newline="",
            encoding="utf-8",
        ) as csvfile:

            writer = csv.writer(csvfile)

            writer.writerow(
                [
                    "events_processed",
                    "accepted_trades",
                    "rejected_trades",
                    "started_at",
                    "finished_at",
                    "elapsed",
                ]
            )

            writer.writerow(
                [
                    report.statistics.events_processed,
                    report.statistics.accepted_trades,
                    report.statistics.rejected_trades,
                    report.statistics.started_at,
                    report.statistics.finished_at,
                    report.statistics.elapsed,
                ]
            )

        #
        # Event history
        #
        events_file = (
            output_directory
            / "runtime_events.csv"
        )

        with events_file.open(
            "w",
            newline="",
            encoding="utf-8",
        ) as csvfile:

            writer = csv.writer(csvfile)

            writer.writerow(
                [
                    "sequence",
                    "timestamp",
                    "accepted",
                ]
            )

            for event in report.events:

                writer.writerow(
                    [
                        event.sequence,
                        event.timestamp,
                        event.accepted,
                    ]
                )