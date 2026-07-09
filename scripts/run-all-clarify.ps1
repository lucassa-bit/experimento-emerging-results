$ErrorActionPreference = "Stop"

# Batch runner for SpecKit clarify experiment collections (Windows).
# For Linux/macOS use scripts/run-all-clarify.sh.
# Workflow: discover runs -> randomize order -> codex exec per run -> write artifacts -> execution-table.csv

# ==========================================================
# CONFIGURATION
# ==========================================================

# Repo root: override with $env:CLARIFY_ROOT or derive from this script location.
$root = if ($env:CLARIFY_ROOT) { $env:CLARIFY_ROOT } else { Split-Path $PSScriptRoot -Parent }

$runsDir = Join-Path $root "runs"
$scriptsDir = Join-Path $root "scripts"
$collectedDir = Join-Path $root "collected-data"
$promptPath = Join-Path $scriptsDir "clarify-prompt.txt"

$executionTablePath = Join-Path $collectedDir "execution-table.csv"

# Short pause between runs
$PauseBetweenRunsSeconds = 3

# --- UTF-8 helpers: all artifacts are read/written as UTF-8 without BOM ---

function Get-Utf8Encoding {
    return [System.Text.UTF8Encoding]::new($false)
}

function Read-Utf8File {
    param([Parameter(Mandatory = $true)][string]$Path)

    return [System.IO.File]::ReadAllText($Path, (Get-Utf8Encoding))
}

function Write-Utf8File {
    param(
        [Parameter(Mandatory = $true)][string]$Path,
        [Parameter(Mandatory = $true)][string]$Content
    )

    [System.IO.File]::WriteAllText($Path, $Content, (Get-Utf8Encoding))
}

function Write-Utf8Lines {
    param(
        [Parameter(Mandatory = $true)][string]$Path,
        [AllowEmptyCollection()]
        [string[]]$Lines = @()
    )

    if ($null -eq $Lines) {
        $Lines = @()
    }

    [System.IO.File]::WriteAllLines($Path, $Lines, (Get-Utf8Encoding))
}

# --- Codex invocation: prompt via stdin, log via cmd redirect (avoids PowerShell deadlock) ---

function Get-CodexExecutablePath {
    $codexCommand = Get-Command codex -ErrorAction Stop

    if ($codexCommand.Source -like "*.cmd") {
        return $codexCommand.Source
    }

    $codexCmd = Join-Path (Split-Path $codexCommand.Source -Parent) "codex.cmd"
    if (Test-Path $codexCmd) {
        return $codexCmd
    }

    return $codexCommand.Source
}

function Get-EscapedProcessArgument {
    param([Parameter(Mandatory = $true)][string]$Value)

    if ($Value -match '[\s"]') {
        return '"' + ($Value -replace '"', '\"') + '"'
    }

    return $Value
}

function Invoke-CodexExec {
    param(
        [Parameter(Mandatory = $true)][string]$RunPath,
        [Parameter(Mandatory = $true)][string]$OutputPath,
        [Parameter(Mandatory = $true)][string]$LogPath,
        [Parameter(Mandatory = $true)][string]$Prompt
    )

    $promptFile = Join-Path $env:TEMP ("codex-prompt-{0}.txt" -f [guid]::NewGuid().ToString("N"))
    $previousErrorAction = $ErrorActionPreference
    $ErrorActionPreference = "Continue"

    $argumentString = @(
        "exec",
        "--cd", (Get-EscapedProcessArgument $RunPath),
        "--sandbox", "read-only",
        "--output-last-message", (Get-EscapedProcessArgument $OutputPath),
        "-"
    ) -join " "

    $codexPath = Get-CodexExecutablePath
    $cmdLine = 'chcp 65001 >nul & "{0}" {1} < "{2}" > "{3}" 2>&1' -f $codexPath, $argumentString, $promptFile, $LogPath

    try {
        Write-Utf8File -Path $promptFile -Content $Prompt

        $process = Start-Process -FilePath "cmd.exe" `
            -ArgumentList @("/c", $cmdLine) `
            -WorkingDirectory $RunPath `
            -NoNewWindow `
            -PassThru `
            -Wait

        return $process.ExitCode
    }
    finally {
        Remove-Item $promptFile -Force -ErrorAction SilentlyContinue
        $ErrorActionPreference = $previousErrorAction
    }
}

# --- Post-processing: build clarification-full.md from codex-log.txt sections ---

function Get-CodexClarificationFullText {
    param(
        [Parameter(Mandatory = $true)]
        [string]$LogPath,

        [Parameter(Mandatory = $true)]
        [string]$OutputPath
    )

    if (-not (Test-Path $LogPath)) {
        throw "codex-log.txt not found: $LogPath"
    }

    if (-not (Test-Path $OutputPath)) {
        throw "output.md not found: $OutputPath"
    }

    $lines = (Read-Utf8File -Path $LogPath) -split "`r?`n"
    $blocks = [System.Collections.Generic.List[string]]::new()
    $current = [System.Collections.Generic.List[string]]::new()
    $inCodex = $false

    foreach ($line in $lines) {
        if ($line -match '^(user|exec|codex)$') {
            if ($inCodex -and $current.Count -gt 0) {
                $blocks.Add(($current -join "`n").Trim())
            }

            $inCodex = ($line -eq 'codex')
            $current.Clear()
            continue
        }

        if ($line -match '^tokens used') {
            break
        }

        if ($inCodex) {
            $current.Add($line)
        }
    }

    if ($inCodex -and $current.Count -gt 0) {
        $blocks.Add(($current -join "`n").Trim())
    }

    if ($blocks.Count -eq 0) {
        throw "No 'codex' messages found in $LogPath"
    }

    $outputContent = (Read-Utf8File -Path $OutputPath).Trim()
    $lastIndex = $blocks.Count - 1

    if ($outputContent -and $blocks[$lastIndex].Contains($outputContent)) {
        $blocks[$lastIndex] = $outputContent
    }

    return ($blocks -join "`n`n---`n`n").Trim()
}

function Write-ClarificationFullFile {
    param(
        [Parameter(Mandatory = $true)]
        [string]$LogPath,

        [Parameter(Mandatory = $true)]
        [string]$OutputPath,

        [Parameter(Mandatory = $true)]
        [string]$ClarificationFullPath
    )

    $fullText = Get-CodexClarificationFullText -LogPath $LogPath -OutputPath $OutputPath
    Write-Utf8File -Path $ClarificationFullPath -Content $fullText
}

function Export-ExecutionTable {
    param([Parameter(Mandatory = $true)][string]$ScriptsDir)

    $pythonCmd = Get-Command python -ErrorAction SilentlyContinue
    if (-not $pythonCmd) {
        $pythonCmd = Get-Command python3 -ErrorAction SilentlyContinue
    }
    if (-not $pythonCmd) {
        Write-Host "WARNING: Python not found; execution-table.csv was not updated."
        return
    }

    & $pythonCmd.Source (Join-Path $ScriptsDir "clarify_runner.py") --build-execution-table | Out-Host
}

# ==========================================================
# INITIAL CHECKS
# ==========================================================

if (-not (Test-Path $root)) {
    throw "Root not found: $root"
}

if (-not (Test-Path $runsDir)) {
    throw "Runs folder not found: $runsDir"
}

if (-not (Test-Path $promptPath)) {
    throw "Prompt not found: $promptPath"
}

New-Item -ItemType Directory -Path $collectedDir -Force | Out-Null

# UTF-8 console avoids mojibake when capturing Codex output on Windows.
chcp 65001 | Out-Null
$utf8 = Get-Utf8Encoding
$OutputEncoding = $utf8
[Console]::OutputEncoding = $utf8
[Console]::InputEncoding = $utf8

$codexCmd = Get-Command codex -ErrorAction SilentlyContinue
if (-not $codexCmd) {
    throw "Command 'codex' not found. Make sure the Codex CLI is installed and on PATH."
}

# ==========================================================
# DISCOVER RUNS
# ==========================================================

$runDirs = Get-ChildItem $runsDir -Directory |
    Where-Object { $_.Name -match '^US\d+_(C0|CL|CO|CD|CS|CT)_R\d+$' }

if ($runDirs.Count -eq 0) {
    throw "No run folders found in $runsDir"
}

# Randomize execution order to reduce ordering bias across conditions.
$orderedRuns = $runDirs | Get-Random -Count $runDirs.Count

$orderRows = foreach ($dir in $orderedRuns) {
    $parts = $dir.Name -split "_"

    [PSCustomObject]@{
        Run_ID = $dir.Name
        US_ID = $parts[0]
        Condition = $parts[1]
        Run_Path = $dir.FullName
    }
}

$totalRuns = $orderRows.Count

Write-Host ""
Write-Host "Total runs: $totalRuns"
Write-Host ""

# ==========================================================
# EXECUTE ALL RUNS
# ==========================================================

$runIndex = 0
$completedCount = 0
$validCount = 0
$failedCount = 0

foreach ($run in $orderRows) {
    $runIndex++
    $remainingCount = $totalRuns - $runIndex

    $runID = $run.Run_ID
    $usID = $run.US_ID
    $condition = $run.Condition
    $runPath = $run.Run_Path

    $specPath = Join-Path $runPath "spec.md"
    $inputDir = Join-Path $runPath "experiment-input"
    $userStoryPath = Join-Path $inputDir "user-story.md"
    $contextPath = Join-Path $inputDir "context.md"

    $outputPath = Join-Path $runPath "output.md"
    $clarificationFullPath = Join-Path $runPath "clarification-full.md"
    $logPath = Join-Path $runPath "codex-log.txt"
    $metadataPath = Join-Path $runPath "metadata.txt"

    Write-Host "=================================================="
    Write-Host "Running: $runID ($runIndex/$totalRuns)"
    Write-Host "US: $usID | Condition: $condition"
    Write-Host "Progress: done=$completedCount | remaining=$remainingCount | valid=$validCount | failed=$failedCount"
    Write-Host "=================================================="

    $status = "Started"
    $errorMessage = ""

    try {
        # Validate experiment inputs before calling Codex.
        if (-not (Test-Path $specPath)) {
            throw "spec.md not found in $runPath"
        }

        if (-not (Test-Path $userStoryPath)) {
            throw "user-story.md not found in $inputDir"
        }

        if ($condition -eq "C0" -and (Test-Path $contextPath)) {
            throw "Condition C0 should not contain context.md: $contextPath"
        }

        if ($condition -ne "C0" -and -not (Test-Path $contextPath)) {
            throw "Condition $condition should contain context.md in $inputDir"
        }

        $existingOutputs = @(
            $outputPath,
            $clarificationFullPath,
            $logPath
        ) | Where-Object { Test-Path $_ }

        if ($existingOutputs.Count -gt 0) {
            Write-Host "Replacing existing files: $($existingOutputs.Count)"
        }

        $start = Get-Date

        @"
Run_ID: $runID
US_ID: $usID
Condition: $condition
Ordem: $runIndex
Start: $($start.ToString("s"))
Run path: $runPath
Prompt path: $promptPath
Status: Started
"@ | Set-Content $metadataPath -Encoding UTF8

        $prompt = Read-Utf8File -Path $promptPath

        Write-Host "Codex running (log: $logPath)..."
        $codexStartedAt = Get-Date

        $exitCode = Invoke-CodexExec `
            -RunPath $runPath `
            -OutputPath $outputPath `
            -LogPath $logPath `
            -Prompt $prompt

        $codexDuration = (Get-Date) - $codexStartedAt
        Write-Host ("Codex finished in {0:mm\:ss}" -f $codexDuration)

        $end = Get-Date

        if ($exitCode -ne 0) {
            throw "codex exec exited with code $exitCode. Check $logPath"
        }

        if (-not (Test-Path $outputPath)) {
            throw "output.md was not created"
        }

        $outputSize = (Get-Item $outputPath).Length

        if ($outputSize -eq 0) {
            throw "output.md was created but is empty"
        }

        # Derive full clarification transcript from the session log.
        Write-ClarificationFullFile -LogPath $logPath -OutputPath $outputPath -ClarificationFullPath $clarificationFullPath

        $status = "Valid"
        $validCount++

        @"
Run_ID: $runID
US_ID: $usID
Condition: $condition
Ordem: $runIndex
Start: $($start.ToString("s"))
End: $($end.ToString("s"))
Run path: $runPath
Prompt path: $promptPath
Output path: $outputPath
Clarification full path: $clarificationFullPath
Log path: $logPath
Status: $status
"@ | Set-Content $metadataPath -Encoding UTF8

        Write-Host "OK: $runID"
    }
    catch {
        $status = "Failed"
        $errorMessage = $_.Exception.Message
        $failedCount++

        $end = Get-Date

        @"
Run_ID: $runID
US_ID: $usID
Condition: $condition
Ordem: $runIndex
End: $($end.ToString("s"))
Run path: $runPath
Prompt path: $promptPath
Output path: $outputPath
Clarification full path: $clarificationFullPath
Log path: $logPath
Status: Failed
Error: $errorMessage
"@ | Set-Content $metadataPath -Encoding UTF8

        Write-Host "FAILED: $runID"
        Write-Host $errorMessage
    }

    $completedCount++

    Export-ExecutionTable -ScriptsDir $scriptsDir

    Write-Host ("Updated progress: done={0}/{1} | remaining={2} | valid={3} | failed={4}" -f $completedCount, $totalRuns, ($totalRuns - $completedCount), $validCount, $failedCount)
    Write-Host ""

    Start-Sleep -Seconds $PauseBetweenRunsSeconds
}

Write-Host ""
Write-Host "=================================================="
Write-Host "EXECUTION FINISHED"
Write-Host ("Total: {0} | Done: {1} | Valid: {2} | Failed: {3}" -f $totalRuns, $completedCount, $validCount, $failedCount)
Write-Host "Execution table saved to:"
Write-Host $executionTablePath
Write-Host "=================================================="
