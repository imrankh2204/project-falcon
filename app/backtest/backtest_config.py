"""
Immutable backtest runtime configuration for Project Falcon.

Defines the immutable runtime parameters required to execute a
backtest. This configuration object contains no business logic and
serves purely as an application-layer value object consumed by the
composition root.

Responsibilities
----------------
- Hold runtime configuration.
- Validate constructor arguments.
- Provide immutable access to configuration values.

The BacktestConfig intentionally does NOT implement:

- Dependency construction
- File validation
- Strategy creation
- Replay orchestration
- Report exporting
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from app.market.instrument import Instrument
from app.market.timeframe import TimeFrame


@dataclass(frozen=True, slots=True)
class BacktestConfig:
    """
    Immutable runtime configuration for a backtest execution.

    Parameters
    ----------
    csv_path
        Path to the historical market data CSV.

    instrument
        Instrument to be traded.

    timeframe
        Timeframe represented by the historical dataset.

    quantity
        Trade quantity for each generated TradeRequest.

    output_directory
        Directory where report exporters may write output.

    export_console
        Enable console report exporter.

    export_csv
        Enable CSV report exporter.

    export_json
        Enable JSON report exporter.
    """

    csv_path: Path
    instrument: Instrument
    timeframe: TimeFrame

    quantity: int

    output_directory: Path

    export_console: bool = True
    export_csv: bool = True
    export_json: bool = True

    def __post_init__(self) -> None:
        """
        Validate configuration values.

        Raises
        ------
        TypeError
            If configuration types are invalid.

        ValueError
            If quantity is not greater than zero.
        """

        if not isinstance(self.csv_path, Path):
            raise TypeError(
                "csv_path must be a pathlib.Path."
            )

        if not isinstance(self.instrument, Instrument):
            raise TypeError(
                "instrument must be an Instrument."
            )

        if not isinstance(self.timeframe, TimeFrame):
            raise TypeError(
                "timeframe must be a TimeFrame."
            )

        if self.quantity <= 0:
            raise ValueError(
                "quantity must be greater than zero."
            )

        if not isinstance(self.output_directory, Path):
            raise TypeError(
                "output_directory must be a pathlib.Path."
            )

        if not isinstance(self.export_console, bool):
            raise TypeError(
                "export_console must be a bool."
            )

        if not isinstance(self.export_csv, bool):
            raise TypeError(
                "export_csv must be a bool."
            )

        if not isinstance(self.export_json, bool):
            raise TypeError(
                "export_json must be a bool."
            )