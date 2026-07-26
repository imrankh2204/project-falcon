"""
Filesystem exporter for Project Falcon optimization reports.

This module provides deterministic persistence of serialized
optimization reports.

Responsibilities
----------------
- Create parent directories.
- Write UTF-8 text files.
- Overwrite existing files deterministically.

The OptimizationExporter intentionally does NOT implement:

- CSV serialization
- JSON serialization
- Optimization logic
- Ranking
"""

from __future__ import annotations

from pathlib import Path


class OptimizationExporter:
    """
    Writes serialized optimization reports to disk.
    """

    def write(
        self,
        *,
        output_path: Path,
        content: str,
    ) -> None:
        """
        Persist serialized report content.

        Parameters
        ----------
        output_path
            Destination file.

        content
            Serialized report text.
        """

        if not isinstance(
            output_path,
            Path,
        ):
            raise TypeError(
                "output_path must be a Path."
            )

        if not isinstance(
            content,
            str,
        ):
            raise TypeError(
                "content must be a string."
            )

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        output_path.write_text(
            content,
            encoding="utf-8",
        )