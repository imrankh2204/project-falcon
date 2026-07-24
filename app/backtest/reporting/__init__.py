"""
Project Falcon reporting subsystem.

This package contains immutable reporting models together with builders and
exporters responsible for presenting completed backtest results.

Public API
----------
BacktestReport
    Immutable reporting model.

ReportBuilder
    Converts BacktestResult into BacktestReport.

ReportExporter
    Common exporter protocol.

ConsoleExporter
    Plain-text report exporter.

CsvExporter
    CSV report exporter.

JsonExporter
    JSON report exporter.
"""

from app.backtest.reporting.builder import ReportBuilder
from app.backtest.reporting.console import ConsoleExporter
from app.backtest.reporting.csv import CsvExporter
from app.backtest.reporting.exporter import ReportExporter
from app.backtest.reporting.json import JsonExporter
from app.backtest.reporting.report import BacktestReport

__all__ = [
    "BacktestReport",
    "ReportBuilder",
    "ReportExporter",
    "ConsoleExporter",
    "CsvExporter",
    "JsonExporter",
]