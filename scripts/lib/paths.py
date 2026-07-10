"""Repository and artifact path helpers."""

from __future__ import annotations

import os
from pathlib import Path


def get_root() -> Path:
    if os.environ.get("CLARIFY_ROOT"):
        return Path(os.environ["CLARIFY_ROOT"]).resolve()
    return Path(__file__).resolve().parent.parent.parent


def scripts_dir() -> Path:
    return get_root() / "scripts"


def gen_dir() -> Path:
    return scripts_dir() / "clarification-gen"


def runs_dir() -> Path:
    return get_root() / "runs"


def collected_dir() -> Path:
    return get_root() / "collected-data"


def prompt_path() -> Path:
    return gen_dir() / "clarify-prompt.txt"


def execution_table_path() -> Path:
    return collected_dir() / "execution-table.csv"

def questions_raw_csv_path() -> Path:
    return collected_dir() / "questions_raw.csv"


def classification_base_csv_path() -> Path:
    return collected_dir() / "classification_base.csv"


def outputs_check_csv_path() -> Path:
    return collected_dir() / "outputs-check.csv"
