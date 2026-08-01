"""
Project Falcon

FAL-580-R3

Runtime Export Validation
"""

from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path
import shutil

from app.live.runtime_csv_exporter import RuntimeCsvExporter
from app.live.runtime_event import RuntimeEvent
from app.live.runtime_json_exporter import RuntimeJsonExporter
from app.live.runtime_session_report import RuntimeSessionReport
from app.live.runtime_statistics import RuntimeStatistics


def main() -> None:

    output_directory = Path("runtime_export_test")

    if output_directory.exists():
        shutil.rmtree(output_directory)

    output_directory.mkdir()

    statistics = RuntimeStatistics(
        events_processed=3,
        accepted_trades=2,
        rejected_trades=1,
        started_at=datetime.now(),
        finished_at=datetime.now(),
        elapsed=timedelta(seconds=5),
    )

    events = (
        RuntimeEvent(
            sequence=1,
            timestamp=datetime.now(),
            accepted=True,
            description="BUY signal accepted",
        ),
        RuntimeEvent(
            sequence=2,
            timestamp=datetime.now(),
            accepted=False,
            description="Risk manager rejected trade",
        ),
        RuntimeEvent(
            sequence=3,
            timestamp=datetime.now(),
            accepted=True,
            description="SELL signal accepted",
        ),
    )

    report = RuntimeSessionReport(
        statistics=statistics,
        events=events,
    )

    RuntimeJsonExporter().export(
        report,
        output_directory / "runtime_report.json",
    )

    RuntimeCsvExporter().export(
        report,
        output_directory,
    )

    assert (
        output_directory / "runtime_report.json"
    ).exists()

    print("PASS: JSON export created")

    assert (
        output_directory / "runtime_statistics.csv"
    ).exists()

    print("PASS: Statistics CSV created")

    assert (
        output_directory / "runtime_events.csv"
    ).exists()

    print("PASS: Events CSV created")

    print()

    print("FAL-580 COMPLETE")


if __name__ == "__main__":
    main()