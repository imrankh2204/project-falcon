"""
Project Falcon

FAL-550-R1

Replay Runtime Validation

Validates that LiveRuntime can consume a deterministic stream of
events from an event source.

The test intentionally uses simple mock components to verify runtime
orchestration only.
"""

from __future__ import annotations

from app.live.live_runtime import LiveRuntime


# ---------------------------------------------------------
# Mock LiveEngine
# ---------------------------------------------------------


class MockLiveEngine:
    """
    Records every processed event.
    """

    def __init__(self) -> None:
        self.events = []

    def start(self) -> None:
        pass

    def stop(self) -> None:
        pass

    def process_event(self, event):
        self.events.append(event)
        print(f"PASS: {event}")


# ---------------------------------------------------------
# Mock Event Source
# ---------------------------------------------------------


class MockEventSource:
    """
    Deterministic event generator.
    """

    def start(self) -> None:
        print("PASS: Replay started")

    def stop(self) -> None:
        print("PASS: Replay completed")

    def events(self):
        yield "Event 1 processed"
        yield "Event 2 processed"
        yield "Event 3 processed"


# ---------------------------------------------------------
# Validation
# ---------------------------------------------------------


def main():

    engine = MockLiveEngine()

    runtime = LiveRuntime(
        live_engine=engine,
        event_source=MockEventSource(),
    )

    print("PASS: Runtime created")

    runtime.run()

    print("PASS: Runtime finished")

    assert len(engine.events) == 3

    print()
    print("FAL-550-R1 COMPLETE")


if __name__ == "__main__":
    main()