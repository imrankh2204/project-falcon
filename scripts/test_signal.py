"""
Project Falcon Signal Test
"""

from app.strategies.signal import Signal


def main() -> None:
    print("=" * 50)
    print("Project Falcon Signal Test")
    print("=" * 50)

    print(f"Buy  : {Signal.BUY}")
    print(f"Sell : {Signal.SELL}")
    print(f"Hold : {Signal.HOLD}")

    assert Signal.BUY.value == "BUY"
    assert Signal.SELL.value == "SELL"
    assert Signal.HOLD.value == "HOLD"

    print("\nSTATUS : PASS")


if __name__ == "__main__":
    main()