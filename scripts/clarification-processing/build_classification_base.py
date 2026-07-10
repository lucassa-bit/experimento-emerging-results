"""Build classification_base.csv from questions_raw.csv."""

from __future__ import annotations

import sys

from lib.io import export_csv, import_csv
from lib.paths import classification_base_csv_path, get_root, questions_raw_csv_path

CLASSIFICATION_FIELDS = [
    "Classification_ID",
    "Run_ID",
    "US_ID",
    "Condition",
    "Question_ID",
    "Segment_ID",
    "Question_Original",
    "Gap_Normalized",
    "Contextual_Category",
    "Coverage",
    "Functional_Relevance",
    "Evidence",
    "Justification",
    "Judge_ID",
    "Adjudication_Status",
]


def build_classification_rows(questions: list[dict[str, str]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    classification_index = 1

    for question in questions:
        if question.get("Question_ID", "") == "NONE":
            continue

        rows.append(
            {
                "Classification_ID": f"CLS{classification_index:04d}",
                "Run_ID": question.get("Run_ID", ""),
                "US_ID": question.get("US_ID", ""),
                "Condition": question.get("Condition", ""),
                "Question_ID": question.get("Question_ID", ""),
                "Segment_ID": "S01",
                "Question_Original": question.get("Question_Original", ""),
                "Gap_Normalized": "",
                "Contextual_Category": "",
                "Coverage": "",
                "Functional_Relevance": "",
                "Evidence": "",
                "Justification": "",
                "Judge_ID": "",
                "Adjudication_Status": "Pending",
            }
        )
        classification_index += 1

    return rows


def main() -> int:
    try:
        get_root()
        input_path = questions_raw_csv_path()
        questions = import_csv(input_path)
        rows = build_classification_rows(questions)
        output_path = classification_base_csv_path()
        export_csv(output_path, rows)

        print(f"Input: {input_path}")
        print(f"Output saved to:\n{output_path}")
        print(f"Total classification rows: {len(rows)}")
        return 0
    except Exception as exc:  # noqa: BLE001
        print(f"Fatal error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
