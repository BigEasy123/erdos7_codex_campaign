# Validate repository-relative paths in theorem files
# This hook rejects absolute paths in theorem-critical files to ensure portability
# Usage: Called after modifying docs/GATE1_*.md or coordination/referee_queue/**

$ErrorActionPreference = "Stop"

function Validate-Relative-Paths {
    param(
        [string]$FilePath
    )
    
    $absolutePathPatterns = @(
        '/mnt/data',
        'C:',
        'D:',
        '/home/user',
        '/root',
        '/tmp'
    )
    
    $content = Get-Content $FilePath -Raw
    $lines = $content -split '\n'
    
    $violations = @()
    $lineNum = 0
    
    foreach ($line in $lines) {
        $lineNum++
        
        # Skip comments and markdown links
        if ($line -match '^\s*#' -or $line -match '^\s*`') {
            continue
        }
        
        foreach ($pattern in $absolutePathPatterns) {
            if ($line -like "*$pattern*") {
                $violations += @{
                    Line   = $lineNum
                    Text   = $line.Trim()
                    Pattern = $pattern
                }
            }
        }
    }
    
    if ($violations.Count -gt 0) {
        Write-Host "✗ ABSOLUTE PATHS FOUND in $FilePath"
        foreach ($violation in $violations) {
            Write-Host "  Line $($violation.Line): $($violation.Pattern)"
            Write-Host "    $($violation.Text)"
        }
        return $false
    }
    
    Write-Host "✓ Path validation PASS: $FilePath"
    return $true
}

$gitRoot = (git rev-parse --show-toplevel 2>$null) ?? (Get-Location).Path

# Target files: docs/GATE1_*.md and coordination/referee_queue/**
$targetPatterns = @(
    "docs/GATE1_*.md",
    "coordination/referee_queue/**"
)

$changedFiles = @()
try {
    $gitStatus = git diff --name-only --cached --diff-filter=ACM 2>$null
    if ($gitStatus) {
        foreach ($file in ($gitStatus -split '\n')) {
            foreach ($pattern in $targetPatterns) {
                if ($file -like $pattern) {
                    $changedFiles += $file
                    break
                }
            }
        }
    }
} catch {
    Write-Host "⚠ Warning: Could not get git status: $_"
}

if ($changedFiles.Count -eq 0) {
    Write-Host "No theorem files changed. Skipping path validation."
    exit 0
}

$failCount = 0
foreach ($file in $changedFiles) {
    $fullPath = Join-Path $gitRoot $file
    if (Test-Path $fullPath) {
        if (-not (Validate-Relative-Paths $fullPath)) {
            $failCount++
        }
    }
}

if ($failCount -gt 0) {
    Write-Host "`n✗ HOOK FAILED: $failCount file(s) with absolute paths"
    exit 1
}

Write-Host "`n✓ Repository path validation passed"
exit 0
