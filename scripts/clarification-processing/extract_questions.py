"""Extract clarification questions from run output.md files."""

from __future__ import annotations

import re
import sys

from lib.io import export_csv
from lib.paths import get_root, questions_raw_csv_path, runs_dir
from lib.runs import RUN_DIR_PATTERN

NEEDS_CLARIFICATION_PATTERN = re.compile(
    r"\[NEEDS CLARIFICATION[^\]]*\]\s*:?\s*(?P<q>[^\r\n]+)",
    re.IGNORECASE,
)
BULLET_PREFIX = re.compile(r"^\s*[-*]\s*")
NUMBER_PREFIX = re.compile(r"^\s*\d+[\).\:\-]\s*")
Q_PREFIX = re.compile(r"^\s*Q\d+[\).\:\-]\s*")
BOLD_WRAPPER = re.compile(r"^\s*\*\*|\*\*$")


def clean_question_line(line: str) -> str:
    cleaned = BULLET_PREFIX.sub("", line)
    cleaned = NUMBER_PREFIX.sub("", cleaned)
    cleaned = Q_PREFIX.sub("", cleaned)
    cleaned = BOLD_WRAPPER.sub("", cleaned)
    return cleaned.strip()


def extract_questions_from_text(text: str) -> list[str]:
    candidates: list[str] = []

    for match in NEEDS_CLARIFICATION_PATTERN.finditer(text):
        question = match.group("q").strip()
        if question:
            candidates.append(question)

    for line in text.splitlines():
        stripped = line.strip()
        if not stripped.endswith("?"):
            continue
        cleaned = clean_question_line(stripped)
        if cleaned:
            candidates.append(cleaned)

    seen: set[str] = set()
    unique: list[str] = []
    for question in candidates:
        key = question.lower()
        if key not in seen:
            seen.add(key)
            unique.append(question)
    return unique


def build_question_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []

    for entry in sorted(runs_dir().iterdir()):
        if not entry.is_dir() or not RUN_DIR_PATTERN.match(entry.name):
            continue

        run_id = entry.name
        us_id, condition, _round = run_id.split("_", 2)
        output_path = entry / "output.md"
        if not output_path.is_file():
            continue

        text = output_path.read_text(encoding="utf-8")
        questions = extract_questions_from_text(text)
        source_file = f"runs\\{run_id}\\output.md"

        if not questions and "NO_CLARIFICATION_NEEDED" in text:
            rows.append(
                {
                    "Run_ID": run_id,
                    "US_ID": us_id,
                    "Condition": condition,
                    "Question_ID": "NONE",
                    "Question_Original": "NO_CLARIFICATION_NEEDED",
                    "Source_File": source_file,
                    "Review_Status": "Check",
                }
            )
            continue

        for index, question in enumerate(questions, start=1):
            rows.append(
                {
                    "Run_ID": run_id,
                    "US_ID": us_id,
                    "Condition": condition,
                    "Question_ID": f"Q{index:02d}",
                    "Question_Original": question,
                    "Source_File": source_file,
                    "Review_Status": "Check",
                }
            )

    return rows


def main() -> int:
    try:
        get_root()
        rows = build_question_rows()
        output_path = questions_raw_csv_path()
        export_csv(output_path, rows)
        print(f"Output saved to:\n{output_path}")
        print(f"Total rows extracted: {len(rows)}")
        return 0
    except Exception as exc:  # noqa: BLE001
        print(f"Fatal error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
