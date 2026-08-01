"""
Project Falcon

FAL-590

Runtime Persistence Validation
"""

from __future__ import annotations

from datetime import datetime, timedelta

from app.live.runtime_event import RuntimeEvent
from app.live.runtime_persistence_service import (
    RuntimePersistenceService,
)
from app.live.runtime_session_report import (
    RuntimeSessionReport,
)
from app.live.runtime_statistics import (
    RuntimeStatistics,
)


class FakeRepository:
    """
    In-memory repository used for validation.
    """

    def __init__(self):

        self.saved_report = None

    def save(
        self,
        report,
    ):
        self.saved_report = report
        return report


def main():

    statistics = RuntimeStatistics(
        events_processed=3,
        accepted_trades=2,
        rejected_trades=1,
        started_at=datetime.now(),
        finished_at=datetime.now(),
        elapsed=timedelta(seconds=2),
    )

    events = (
        RuntimeEvent(
            sequence=1,
            timestamp=datetime.now(),
            accepted=True,
            description="BUY signal processed",
        ),
        RuntimeEvent(
            sequence=2,
            timestamp=datetime.now(),
            accepted=False,
            description="Risk rejected",
        ),
    )

    report = RuntimeSessionReport(
        statistics=statistics,
        events=events,
    )

    repository = FakeRepository()

    service = RuntimePersistenceService(
        repository=repository,
    )

    persisted = service.persist(
        report,
    )

    assert persisted is report

    print(
        "PASS: RuntimeSessionReport persisted"
    )

    assert repository.saved_report is report

    print(
        "PASS: Repository invoked"
    )

    assert (
        repository.saved_report.statistics.events_processed
        == 3
    )

    print(
        "PASS: Stored report verified"
    )

    print()

    print(
        "FAL-590 COMPLETE"
    )


if __name__ == "__main__":
    main()