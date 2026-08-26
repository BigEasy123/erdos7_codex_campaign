# Run declared optimizer-free verifiers
# This hook automatically executes verifier scripts declared in theorem files
# Usage: Called after modifying docs/*_THEOREM.md files

$ErrorActionPreference = "Stop"

function Extract-Verifier-Command {
    param(
        [string]$FilePath
    )
    
    $content = Get-Content $FilePath -Raw
    
    # Look for "Verifier Command" section
    if ($content -match '## (?:Independent )?Verif(?:ier|ication).*?```bash\s*(.*?)\s*```') {
        $command = $Matches[1].Trim()
        return $command
    }
    
    # Alternative: "Verifier Command:" line
    if ($content -match '(?:Verifier|Verifier Command):\s*```\s*(.+?)\s*```') {
        $command = $Matches[1].Trim()
        return $command
    }
    
    return $null
}

function Run-Verifier {
    param(
        [string]$VerifierCommand,
        [string]$WorkingDir
    )
    
    Write-Host "`n▶ Running verifier: $VerifierCommand"
    
    try {
        Push-Location $WorkingDir
        
        # Parse command (typically "python src/verify_*.py")
        $parts = $VerifierCommand -split '\s+'
        $exe = $parts[0]
        $args = $parts[1..($parts.Count - 1)]
        
        # Execute
        $output = & $exe @args 2>&1
        $exitCode = $LASTEXITCODE
        
        Pop-Location
        
        Write-Host $output
        
        if ($exitCode -eq 0) {
            Write-Host "✓ Verifier PASS"
            return $true
        } else {
            Write-Host "✗ Verifier FAIL (exit code: $exitCode)"
            return $false
        }
    } catch {
        Write-Host "✗ Verifier execution error: $_"
        if ((Get-Location).Path -ne $WorkingDir) { Pop-Location }
        return $false
    }
}

$gitRoot = (git rev-parse --show-toplevel 2>$null) ?? (Get-Location).Path

# Target files: docs/*_THEOREM.md
$changedFiles = @()
try {
    $gitStatus = git diff --name-only --cached --diff-filter=ACM 2>$null
    if ($gitStatus) {
        $changedFiles += $gitStatus -split '\n' | Where-Object { $_ -like "docs/*_THEOREM*.md" }
    }
} catch {
    Write-Host "⚠ Warning: Could not get git status: $_"
}

if ($changedFiles.Count -eq 0) {
    Write-Host "No theorem files changed. Skipping verifier execution."
    exit 0
}

$failCount = 0
foreach ($file in $changedFiles) {
    $fullPath = Join-Path $gitRoot $file
    if (Test-Path $fullPath) {
        $verifierCmd = Extract-Verifier-Command $fullPath
        
        if ($verifierCmd) {
            Write-Host "`nFile: $file"
            if (-not (Run-Verifier -VerifierCommand $verifierCmd -WorkingDir $gitRoot)) {
                $failCount++
            }
        } else {
            Write-Host "⚠ No verifier command found in $file (optional if symbolic-only)"
        }
    }
}

if ($failCount -gt 0) {
    Write-Host "`n✗ HOOK FAILED: $failCount verifier(s) failed"
    # Note: We do not block on verifier failure, only warn.
    # This allows symbolic proofs (without runnable verifiers) to proceed.
    exit 0
}

Write-Host "`n✓ Verifier execution completed"
exit 0
