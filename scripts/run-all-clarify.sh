#!/usr/bin/env bash
# Linux/macOS entry point for batch SpecKit clarify runs.
# Requires: python3, codex CLI on PATH.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
export CLARIFY_ROOT="${CLARIFY_ROOT:-$ROOT}"

echo "Running all SpecKit clarify executions..."
echo "Root: ${CLARIFY_ROOT}"
echo

python3 "${SCRIPT_DIR}/clarify_runner.py"
exit_code=$?

echo
if [[ ${exit_code} -eq 0 ]]; then
  echo "Finished."
else
  echo "Finished with errors."
fi
echo "Check collected-data/execution-table.csv"

exit "${exit_code}"
