# Validate SHA256 hashes for exact artifacts
# This hook verifies that newly created artifacts in artifacts/exact/ have valid SHA256 records
# Usage: Called after file creation/modification in artifacts/exact/

$ErrorActionPreference = "Stop"

function Validate-Artifact-SHA256 {
    param(
        [string]$FilePath
    )
    
    # Compute current SHA256
    $computedHash = (Get-FileHash -Path $FilePath -Algorithm SHA256).Hash.ToLower()
    
    # Look for .sha256 record file
    $sha256File = "$FilePath.sha256"
    
    if (Test-Path $sha256File) {
        # Read recorded hash
        $recordedHash = (Get-Content $sha256File).Trim().ToLower()
        
        if ($computedHash -eq $recordedHash) {
            Write-Host "✓ SHA256 PASS: $FilePath"
            return $true
        } else {
            Write-Host "✗ SHA256 MISMATCH: $FilePath"
            Write-Host "  Expected: $recordedHash"
            Write-Host "  Got:      $computedHash"
            return $false
        }
    } else {
        # No record file yet; log the hash for inspection
        Write-Host "⚠ SHA256 RECORD MISSING: $FilePath"
        Write-Host "  Computed hash (save to $sha256File if intentional):"
        Write-Host "  $computedHash"
        
        # Do not fail; just warn. Author should commit .sha256 file.
        return $true
    }
}

# Get all modified/created files in artifacts/exact/
$gitRoot = (git rev-parse --show-toplevel 2>$null) ?? (Get-Location).Path
$artifactDir = Join-Path $gitRoot "artifacts" "exact"

if (-not (Test-Path $artifactDir)) {
    Write-Host "No artifacts/exact/ directory found. Skipping SHA256 validation."
    exit 0
}

# Check staged/modified files
$changedFiles = @()
try {
    $gitStatus = git diff --name-only --cached --diff-filter=ACM 2>$null
    if ($gitStatus) {
        $changedFiles += $gitStatus -split '\n' | Where-Object { $_ -like "artifacts/exact/*" }
    }
} catch {
    Write-Host "⚠ Warning: Could not get git status: $_"
}

if ($changedFiles.Count -eq 0) {
    Write-Host "No changes in artifacts/exact/. Skipping."
    exit 0
}

$failCount = 0
foreach ($file in $changedFiles) {
    $fullPath = Join-Path $gitRoot $file
    if (Test-Path $fullPath) {
        if (-not (Validate-Artifact-SHA256 $fullPath)) {
            $failCount++
        }
    }
}

if ($failCount -gt 0) {
    Write-Host "`n✗ HOOK FAILED: $failCount SHA256 mismatch(es)"
    # Exit with non-zero to block the operation
    exit 1
}

Write-Host "`n✓ SHA256 validation passed"
exit 0
