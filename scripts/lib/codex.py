"""Codex CLI resolution helpers."""

from __future__ import annotations

import os
import shutil
import sys


def resolve_codex_executable() -> str:
    """Return an absolute Codex executable path usable with subprocess."""
    if sys.platform == "win32":
        for candidate in ("codex.cmd", "codex.exe", "codex"):
            resolved = shutil.which(candidate)
            if resolved:
                return os.path.abspath(resolved)

    resolved = shutil.which("codex")
    if resolved:
        return os.path.abspath(resolved)

    raise RuntimeError("Command 'codex' not found. Install the Codex CLI and add it to PATH.")


def ensure_codex_available() -> str:
    return resolve_codex_executable()
