@echo off
title Run all SpecKit Clarify executions

set ROOT=%~dp0
set ROOT=%ROOT:~0,-1%
set CLARIFY_ROOT=%ROOT%

echo Running all SpecKit clarify executions...
echo Root: %ROOT%
echo.

powershell -ExecutionPolicy Bypass -NoProfile -File "%ROOT%\scripts\run-all-clarify.ps1"

echo.
echo Finished.
echo Check collected-data\execution-table.csv
pause