"""
Project Falcon Kite SDK Validation
"""

from kiteconnect import KiteConnect


def main() -> None:
    print("=" * 50)
    print("Project Falcon Kite SDK Test")
    print("=" * 50)

    print("KiteConnect imported successfully.")
    print(f"Class Name : {KiteConnect.__name__}")

    print()
    print("STATUS : PASS")


if __name__ == "__main__":
    main()