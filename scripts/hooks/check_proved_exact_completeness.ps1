# Check PROVED_EXACT theorems for required completeness
# This hook verifies that theorems marked PROVED_EXACT include both SHA256 hash and verifier command
# Usage: Called after modifying theorem files

$ErrorActionPreference = "Stop"

function Check-Proved-Exact-Completeness {
    param(
        [string]$FilePath
    )
    
    $content = Get-Content $FilePath -Raw
    
    # Check if this is marked as PROVED_EXACT
    if ($content -notmatch 'Status.*PROVED_EXACT') {
        # Not PROVED_EXACT, skip
        return @{
            IsProvedExact = $false
            Violations = @()
        }
    }
    
    $violations = @()
    
    # Requirement 1: Must have a Verifier Command section
    if ($content -notmatch '(?:## (?:Independent )?Verif(?:ier|ication)|Verifier Command)') {
        $violations += "Missing 'Verifier Command' or 'Independent Verification' section"
    }
    
    # Requirement 2: Must have at least one SHA256 hash entry
    if ($content -notmatch '[0-9a-fA-F]{64}') {
        $violations += "Missing SHA256 hash(es) in Artifacts section"
    }
    
    # Requirement 3: Must have explicit hypothesis list
    if ($content -notmatch '## Hypothes[ei]s') {
        $violations += "Missing explicit 'Hypotheses' section"
    }
    
    # Requirement 4: Must have dependency audit checklist
    if ($content -notmatch '## .*Dependenc[iy]|## .*Audit.*Checklist') {
        $violations += "Missing 'Dependencies' or 'Dependency Audit Checklist' section"
    }
    
    # Requirement 5: Verifier must not reference optimizer
    if ($content -match 'Verifier.*:.*' -and $content -match '(SciPy|Gurobi|CPLEX|HiGHS)') {
        if ($content -match 'No (?:SciPy|optimizer)' -or $content -match 'optimizer.free') {
            # OK, explicitly says no optimizer
        } else {
            $violations += "Verifier section mentions optimizer without explicit 'optimizer-free' disclaimer"
        }
    }
    
    return @{
        IsProvedExact = $true
        Violations = $violations
    }
}

$gitRoot = (git rev-parse --show-toplevel 2>$null) ?? (Get-Location).Path

# Target files: docs/**THEOREM*.md
$changedFiles = @()
try {
    $gitStatus = git diff --name-only --cached --diff-filter=ACM 2>$null
    if ($gitStatus) {
        $changedFiles += $gitStatus -split '\n' | Where-Object { $_ -like "docs/*THEOREM*.md" }
    }
} catch {
    Write-Host "⚠ Warning: Could not get git status: $_"
}

if ($changedFiles.Count -eq 0) {
    Write-Host "No theorem files changed. Skipping completeness check."
    exit 0
}

$failCount = 0
foreach ($file in $changedFiles) {
    $fullPath = Join-Path $gitRoot $file
    if (Test-Path $fullPath) {
        $result = Check-Proved-Exact-Completeness $fullPath
        
        if ($result.IsProvedExact) {
            if ($result.Violations.Count -gt 0) {
                Write-Host "✗ PROVED_EXACT INCOMPLETE: $file"
                foreach ($violation in $result.Violations) {
                    Write-Host "  - $violation"
                }
                $failCount++
            } else {
                Write-Host "✓ PROVED_EXACT complete: $file"
            }
        }
    }
}

if ($failCount -gt 0) {
    Write-Host "`n✗ HOOK FAILED: $failCount PROVED_EXACT theorem(s) missing required sections"
    exit 1
}

Write-Host "`n✓ PROVED_EXACT completeness check passed"
exit 0
