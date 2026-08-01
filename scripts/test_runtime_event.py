"""
Project Falcon

FAL-560-R1

Runtime Event Validation
"""

from __future__ import annotations

from datetime import datetime

from app.live.runtime_event import RuntimeEvent


def main() -> None:

    event = RuntimeEvent(
        sequence=1,
        timestamp=datetime.now(),
        accepted=True,
        description="Trade accepted",
    )

    assert event.sequence == 1
    assert event.accepted is True
    assert event.description == "Trade accepted"

    print("PASS: RuntimeEvent created")

    print()

    print("FAL-560-R1 COMPLETE")


if __name__ == "__main__":
    main()