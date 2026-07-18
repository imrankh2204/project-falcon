"""
Project Falcon TimeFrame Validation
"""

from app.market.timeframe import TimeFrame


def main() -> None:
    print("=" * 50)
    print("Project Falcon TimeFrame Test")
    print("=" * 50)

    print("\nSupported TimeFrames\n")

    for timeframe in TimeFrame:
        print(timeframe.value)

    print(f"\nTotal Supported : {len(TimeFrame)}")

    values = TimeFrame.values()

    assert len(values) == len(set(values)), (
        "Duplicate timeframe values detected."
    )

    print("\nSTATUS : PASS")


if __name__ == "__main__":
    main()