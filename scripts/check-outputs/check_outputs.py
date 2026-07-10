"""Check whether each run folder has a non-empty output.md."""

from __future__ import annotations

import sys

from lib.io import export_csv
from lib.paths import get_root, outputs_check_csv_path, runs_dir
from lib.runs import RUN_DIR_PATTERN


def build_output_check_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    for entry in sorted(runs_dir().iterdir()):
        if not entry.is_dir() or not RUN_DIR_PATTERN.match(entry.name):
            continue

        output_path = entry / "output.md"
        exists = output_path.is_file()
        rows.append(
            {
                "Run_ID": entry.name,
                "Output_Exists": exists,
                "Output_Size_Bytes": output_path.stat().st_size if exists else 0,
                "Output_Path": str(output_path),
            }
        )

    return rows


def main() -> int:
    try:
        get_root()
        rows = build_output_check_rows()
        output_path = outputs_check_csv_path()
        export_csv(output_path, rows)
        print(f"Output saved to:\n{output_path}")
        print(f"Total runs checked: {len(rows)}")
        return 0
    except Exception as exc:  # noqa: BLE001
        print(f"Fatal error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
