"""
Project Falcon OptionType Validation
"""

from app.market.option_type import OptionType


def main() -> None:
    print("=" * 50)
    print("Project Falcon OptionType Test")
    print("=" * 50)

    print()

    for option in OptionType:
        print(option.value)

    values = OptionType.values()

    assert values == ["CE", "PE"]

    print("\nTotal Supported :", len(values))

    print("\nSTATUS : PASS")


if __name__ == "__main__":
    main()