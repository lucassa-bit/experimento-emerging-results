from __future__ import annotations

import csv
import os
import random
import re
import shutil
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

RUN_DIR_PATTERN = re.compile(r"^US\d+_(C0|CL|CO|CD|CS|CT)_R\d+$")
REPETITION_PATTERN = re.compile(r"_R(\d+)$")
PAUSE_BETWEEN_RUNS_SECONDS = 3

EXECUTION_TABLE_FIELDS = [
    "Run_ID",
    "US_ID",
    "Condicao",
    "Repeticao",
    "Ordem",
    "Data_hora",
    "Arquivo_saida",
    "Status",
    "Erro",
]


@dataclass
class RunInfo:
    run_id: str
    us_id: str
    condition: str
    run_path: Path


def get_root() -> Path:
    if os.environ.get("CLARIFY_ROOT"):
        return Path(os.environ["CLARIFY_ROOT"]).resolve()
    return Path(__file__).resolve().parent.parent


def read_utf8(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_utf8(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8", newline="\n")


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
        raise FileNotFoundError(f"Condition {run.condition} should contain context.md in {context_path.parent}")


def invoke_codex_exec(run_path: Path, output_path: Path, log_path: Path, prompt: str) -> int:
    """Run codex with prompt on stdin; merge stdout/stderr into the log file."""
    env = os.environ.copy()
    env.setdefault("LC_ALL", "C.UTF-8")
    env.setdefault("LANG", "C.UTF-8")

    with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False) as prompt_file:
        prompt_file.write(prompt)
        prompt_file_path = prompt_file.name

    try:
        with log_path.open("w", encoding="utf-8") as log_file, Path(prompt_file_path).open(
            "r", encoding="utf-8"
        ) as stdin_file:
            result = subprocess.run(
                [
                    "codex",
                    "exec",
                    "--cd",
                    str(run_path),
                    "--sandbox",
                    "read-only",
                    "--output-last-message",
                    str(output_path),
                    "-",
                ],
                stdin=stdin_file,
                stdout=log_file,
                stderr=subprocess.STDOUT,
                cwd=run_path,
                env=env,
                check=False,
            )
        return result.returncode
    finally:
        Path(prompt_file_path).unlink(missing_ok=True)


def extract_clarification_full_text(log_path: Path, output_path: Path) -> str:
    lines = read_utf8(log_path).splitlines()
    blocks: list[str] = []
    current: list[str] = []
    in_codex = False

    for line in lines:
        if line in {"user", "exec", "codex"}:
            if in_codex and current:
                blocks.append("\n".join(current).strip())
            in_codex = line == "codex"
            current = []
            continue
        if line.startswith("tokens used"):
            break
        if in_codex:
            current.append(line)

    if in_codex and current:
        blocks.append("\n".join(current).strip())

    if not blocks:
        raise ValueError(f"No 'codex' messages found in {log_path}")

    output_content = read_utf8(output_path).strip()
    if output_content and output_content in blocks[-1]:
        blocks[-1] = output_content

    return "\n\n---\n\n".join(blocks).strip()


def write_metadata(path: Path, fields: dict[str, str]) -> None:
    content = "\n".join(f"{key}: {value}" for key, value in fields.items())
    write_utf8(path, content + "\n")


def export_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()), quoting=csv.QUOTE_ALL)
        writer.writeheader()
        writer.writerows(rows)


def ensure_codex_available() -> None:
    if shutil.which("codex") is None:
        raise RuntimeError("Command 'codex' not found. Install the Codex CLI and add it to PATH.")


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


def read_metadata(path: Path) -> dict[str, str]:
    if not path.is_file():
        return {}

    fields: dict[str, str] = {}
    for line in read_utf8(path).splitlines():
        if ": " in line:
            key, value = line.split(": ", 1)
            fields[key.strip()] = value.strip()
    return fields


def build_execution_row(
    run: RunInfo,
    metadata: dict[str, str],
    *,
    ordem: str | int = "",
    in_execution_order: bool = False,
) -> dict[str, object]:
    internal_status = metadata.get("Status", "")
    clarification_full_path = run.run_path / "clarification-full.md"
    arquivo_saida = str(clarification_full_path) if clarification_full_path.is_file() else ""

    return {
        "Run_ID": run.run_id,
        "US_ID": run.us_id,
        "Condicao": run.condition,
        "Repeticao": parse_repeticao(run.run_id),
        "Ordem": ordem if ordem != "" else metadata.get("Ordem", ""),
        "Data_hora": metadata.get("End") or metadata.get("Start", ""),
        "Arquivo_saida": arquivo_saida,
        "Status": map_status_pt(internal_status, in_execution_order=in_execution_order),
        "Erro": metadata.get("Error", ""),
    }


def build_execution_table(root: Path) -> list[dict[str, object]]:
    runs_dir = root / "runs"
    rows: list[dict[str, object]] = []

    for run in discover_runs(runs_dir):
        metadata = read_metadata(run.run_path / "metadata.txt")
        in_order = bool(metadata.get("Ordem"))
        rows.append(build_execution_row(run, metadata, in_execution_order=in_order))

    rows.sort(
        key=lambda row: (
            row["Ordem"] == "",
            int(row["Ordem"]) if str(row["Ordem"]).isdigit() else 999,
            str(row["Run_ID"]),
        )
    )
    return rows


def export_execution_table(root: Path, rows: list[dict[str, object]] | None = None) -> Path:
    collected_dir = root / "collected-data"
    execution_table_path = collected_dir / "execution-table.csv"
    table_rows = rows if rows is not None else build_execution_table(root)
    export_csv(execution_table_path, table_rows)
    return execution_table_path


def run_all(root: Path | None = None) -> list[dict[str, object]]:
    root = root or get_root()
    runs_dir = root / "runs"
    scripts_dir = root / "scripts"
    collected_dir = root / "collected-data"
    prompt_path = scripts_dir / "clarify-prompt.txt"

    if not runs_dir.is_dir():
        raise FileNotFoundError(f"Runs folder not found: {runs_dir}")
    if not prompt_path.is_file():
        raise FileNotFoundError(f"Prompt not found: {prompt_path}")

    ensure_codex_available()
    collected_dir.mkdir(parents=True, exist_ok=True)

    runs = discover_runs(runs_dir)
    if not runs:
        raise RuntimeError(f"No run folders found in {runs_dir}")

    random.shuffle(runs)

    prompt = read_utf8(prompt_path)
    total_runs = len(runs)
    execution_table: list[dict[str, object]] = []
    completed_count = 0
    valid_count = 0
    failed_count = 0

    print(f"\nTotal runs: {total_runs}\n")

    for run_index, run in enumerate(runs, start=1):
        remaining_count = total_runs - run_index
        output_path = run.run_path / "output.md"
        clarification_full_path = run.run_path / "clarification-full.md"
        log_path = run.run_path / "codex-log.txt"
        metadata_path = run.run_path / "metadata.txt"

        print("=" * 50)
        print(f"Running: {run.run_id} ({run_index}/{total_runs})")
        print(f"US: {run.us_id} | Condition: {run.condition}")
        print(
            f"Progress: done={completed_count} | remaining={remaining_count} "
            f"| valid={valid_count} | failed={failed_count}"
        )
        print("=" * 50)

        status = "Started"
        error_message = ""
        start = datetime.now()

        try:
            validate_run_inputs(run)

            existing_outputs = sum(
                1 for path in (output_path, clarification_full_path, log_path) if path.exists()
            )
            if existing_outputs:
                print(f"Replacing existing files: {existing_outputs}")

            write_metadata(
                metadata_path,
                {
                    "Run_ID": run.run_id,
                    "US_ID": run.us_id,
                    "Condition": run.condition,
                    "Ordem": str(run_index),
                    "Start": start.strftime("%Y-%m-%dT%H:%M:%S"),
                    "Run path": str(run.run_path),
                    "Prompt path": str(prompt_path),
                    "Status": "Started",
                },
            )

            print(f"Codex running (log: {log_path})...")
            codex_started_at = time.monotonic()
            exit_code = invoke_codex_exec(run.run_path, output_path, log_path, prompt)
            codex_duration = time.monotonic() - codex_started_at
            print(f"Codex finished in {int(codex_duration // 60):02d}:{int(codex_duration % 60):02d}")

            end = datetime.now()
            if exit_code != 0:
                raise RuntimeError(f"codex exec exited with code {exit_code}. Check {log_path}")
            if not output_path.is_file():
                raise FileNotFoundError("output.md was not created")
            if output_path.stat().st_size == 0:
                raise ValueError("output.md was created but is empty")

            write_utf8(
                clarification_full_path,
                extract_clarification_full_text(log_path, output_path),
            )

            status = "Valid"
            valid_count += 1
            write_metadata(
                metadata_path,
                {
                    "Run_ID": run.run_id,
                    "US_ID": run.us_id,
                    "Condition": run.condition,
                    "Ordem": str(run_index),
                    "Start": start.strftime("%Y-%m-%dT%H:%M:%S"),
                    "End": end.strftime("%Y-%m-%dT%H:%M:%S"),
                    "Run path": str(run.run_path),
                    "Prompt path": str(prompt_path),
                    "Output path": str(output_path),
                    "Clarification full path": str(clarification_full_path),
                    "Log path": str(log_path),
                    "Status": status,
                },
            )
            print(f"OK: {run.run_id}")
        except Exception as exc:  # noqa: BLE001 - batch runner reports and continues
            status = "Failed"
            error_message = str(exc)
            failed_count += 1
            end = datetime.now()
            write_metadata(
                metadata_path,
                {
                    "Run_ID": run.run_id,
                    "US_ID": run.us_id,
                    "Condition": run.condition,
                    "Ordem": str(run_index),
                    "End": end.strftime("%Y-%m-%dT%H:%M:%S"),
                    "Run path": str(run.run_path),
                    "Prompt path": str(prompt_path),
                    "Output path": str(output_path),
                    "Clarification full path": str(clarification_full_path),
                    "Log path": str(log_path),
                    "Status": "Failed",
                    "Error": error_message,
                },
            )
            print(f"FAILED: {run.run_id}")
            print(error_message)

        completed_count += 1
        metadata = read_metadata(metadata_path)
        execution_table.append(
            build_execution_row(run, metadata, ordem=run_index, in_execution_order=True)
        )
        export_execution_table(root, execution_table)

        print(
            f"Updated progress: done={completed_count}/{total_runs} | "
            f"remaining={total_runs - completed_count} | valid={valid_count} | failed={failed_count}\n"
        )
        time.sleep(PAUSE_BETWEEN_RUNS_SECONDS)

    print("\n" + "=" * 50)
    print("EXECUTION FINISHED")
    print(f"Total: {total_runs} | Done: {completed_count} | Valid: {valid_count} | Failed: {failed_count}")
    execution_table_path = export_execution_table(root, execution_table)
    print(f"Execution table saved to:\n{execution_table_path}")
    print("=" * 50)

    return execution_table


def main() -> int:
    try:
        if len(sys.argv) > 1 and sys.argv[1] == "--build-execution-table":
            root = get_root()
            path = export_execution_table(root)
            print(f"Execution table saved to: {path}")
            return 0

        run_all()
        return 0
    except Exception as exc:  # noqa: BLE001
        print(f"Fatal error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
