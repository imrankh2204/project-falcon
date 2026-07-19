"""
Project Falcon Indicator Interface Test
"""

from app.indicators.indicator import Indicator


def main() -> None:
    print("=" * 50)
    print("Project Falcon Indicator Test")
    print("=" * 50)

    print()

    required = [
        "name",
        "calculate",
    ]

    for member in required:
        assert hasattr(Indicator, member)
        print(f"Found : {member}")

    print("\nSTATUS : PASS")


if __name__ == "__main__":
    main()