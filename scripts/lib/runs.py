"""Run discovery and validation."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

RUN_DIR_PATTERN = re.compile(r"^US\d+_(C0|CL|CO|CD|CS|CT)_R\d+$")
REPETITION_PATTERN = re.compile(r"_R(\d+)$")


@dataclass
class RunInfo:
    run_id: str
    us_id: str
    condition: str
    run_path: Path


def discover_runs(runs_dir: Path) -> list[RunInfo]:
    runs: list[RunInfo] = []
    for entry in sorted(runs_dir.iterdir()):
        if not entry.is_dir() or not RUN_DIR_PATTERN.match(entry.name):
            continue
        us_id, condition, _round = entry.name.split("_", 2)
        runs.append(RunInfo(entry.name, us_id, condition, entry))
    return runs


def validate_run_inputs(run: RunInfo) -> None:
    spec_path = run.run_path / "spec.md"
    user_story_path = run.run_path / "experiment-input" / "user-story.md"
    context_path = run.run_path / "experiment-input" / "context.md"

    if not spec_path.is_file():
        raise FileNotFoundError(f"spec.md not found in {run.run_path}")
    if not user_story_path.is_file():
        raise FileNotFoundError(f"user-story.md not found in {user_story_path.parent}")
    if run.condition == "C0" and context_path.exists():
        raise ValueError(f"Condition C0 should not contain context.md: {context_path}")
    if run.condition != "C0" and not context_path.is_file():
        raise FileNotFoundError(
            f"Condition {run.condition} should contain context.md in {context_path.parent}"
        )


def parse_repeticao(run_id: str) -> int:
    match = REPETITION_PATTERN.search(run_id)
    if not match:
        raise ValueError(f"Cannot parse repetition from run id: {run_id}")
    return int(match.group(1))


def map_status_pt(internal_status: str, *, in_execution_order: bool) -> str:
    if internal_status == "Valid":
        return "Valida"
    if internal_status == "Failed":
        return "falha"
    if internal_status == "Started":
        return "incompleta"
    if in_execution_order:
        return "incompleta"
    return "excluída"
