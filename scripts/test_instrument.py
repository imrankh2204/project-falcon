"""
Project Falcon Instrument Validation
"""

from datetime import date

from app.market.instrument import Instrument
from app.market.option_type import OptionType


def main() -> None:
    print("=" * 50)
    print("Project Falcon Instrument Test")
    print("=" * 50)

    equity = Instrument(
        exchange="NSE",
        symbol="RELIANCE",
        instrument_token=738561,
        lot_size=1,
        tick_size=0.05,
    )

    option = Instrument(
        exchange="NFO",
        symbol="NIFTY25JUL25000CE",
        instrument_token=123456,
        lot_size=75,
        tick_size=0.05,
        expiry=date(2026, 7, 30),
        strike=25000.0,
        option_type=OptionType.CALL,
    )

    print(f"Equity : {equity.display_name}")
    print(f"Option : {option.display_name}")

    print()

    print(f"Equity Is Option : {equity.is_option}")
    print(f"Option Is Option : {option.is_option}")

    assert not equity.is_option
    assert option.is_option

    print("\nSTATUS : PASS")


if __name__ == "__main__":
    main()