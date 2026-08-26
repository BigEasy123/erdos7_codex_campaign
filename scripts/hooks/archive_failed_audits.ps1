# Archive failed audits before context compaction
# This hook ensures FAILED/ audit records are preserved before PreCompact
# Usage: Called before compacting session context

$ErrorActionPreference = "Stop"

function Archive-Failed-Audits {
    param(
        [string]$FailedDir,
        [string]$ArchiveDir
    )
    
    if (-not (Test-Path $FailedDir)) {
        Write-Host "No FAILED/ directory found. Nothing to archive."
        return $true
    }
    
    $failedFiles = Get-ChildItem -Path $FailedDir -Filter "*.md" -ErrorAction SilentlyContinue
    
    if ($failedFiles.Count -eq 0) {
        Write-Host "No failed audit records to archive."
        return $true
    }
    
    # Create archive directory if it doesn't exist
    if (-not (Test-Path $ArchiveDir)) {
        New-Item -ItemType Directory -Path $ArchiveDir | Out-Null
    }
    
    foreach ($file in $failedFiles) {
        $timestamp = (Get-Date -Format "yyyyMMdd_HHmmss")
        $archiveName = "$($file.BaseName)_archived_$timestamp$($file.Extension)"
        $archivePath = Join-Path $ArchiveDir $archiveName
        
        Write-Host "Archiving: $($file.Name) → $archiveName"
        Copy-Item -Path $file.FullName -Destination $archivePath -Force | Out-Null
    }
    
    Write-Host "✓ Failed audits archived"
    return $true
}

$gitRoot = (git rev-parse --show-toplevel 2>$null) ?? (Get-Location).Path
$failedDir = Join-Path $gitRoot "coordination" "referee_queue" "FAILED"
$archiveDir = Join-Path $gitRoot "coordination" "referee_queue" "ARCHIVE"

if (Archive-Failed-Audits $failedDir $archiveDir) {
    exit 0
} else {
    Write-Host "✗ Failed to archive audit records"
    exit 1
}
