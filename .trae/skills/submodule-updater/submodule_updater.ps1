# Git Submodule Updater (PowerShell Version)
# Supports updating all submodules or submodules in a specific directory

class SubmoduleUpdater {
    [string]$BaseDir
    [int]$SuccessCount
    [int]$FailureCount
    [datetime]$StartTime

    SubmoduleUpdater() {
        $this.BaseDir = Get-Location
        $this.SuccessCount = 0
        $this.FailureCount = 0
        $this.StartTime = Get-Date
    }

    SubmoduleUpdater([string]$baseDir) {
        $this.BaseDir = $baseDir
        $this.SuccessCount = 0
        $this.FailureCount = 0
        $this.StartTime = Get-Date
    }

    [object] ParseCommand([string]$command) {
        $originalCommand = $command.Trim()
        
        # Check if command contains "下的" (Chinese for "under")
        # Using character positions to avoid encoding issues
        for ($i = 0; $i -lt $originalCommand.Length - 1; $i++) {
            if ($originalCommand[$i] -eq 19979 -and $originalCommand[$i + 1] -eq 30340) {
                # Extract directory path between "更新" and "下的"
                $beforePart = $originalCommand.Substring(0, $i)
                if ($beforePart -match '更新\s*(.+)') {
                    $dirPath = $matches[1].Trim()
                    $dirPath = $dirPath -replace '\\', '/'
                    return @{ UpdateAll = $false; DirPath = $dirPath }
                }
                break
            }
        }
        
        # Pattern 2: Update submodules in specific directory (English patterns)
        $patternsDir = @(
            'update\s+submodules\s+in\s+(.+)',
            'update\s+(.+)\s+submodules'
        )
        
        foreach ($pattern in $patternsDir) {
            if ($originalCommand -match $pattern) {
                $dirPath = $matches[1].Trim()
                $dirPath = $dirPath -replace '\\', '/'
                return @{ UpdateAll = $false; DirPath = $dirPath }
            }
        }
        
        # Pattern 1: Update all submodules (check this after directory patterns)
        $patternsAll = @(
            '更新所有submodule',
            '更新全部submodule',
            'update\s+all\s+submodules',
            'update\s+every\s+submodule'
        )
        
        foreach ($pattern in $patternsAll) {
            if ($originalCommand -match $pattern) {
                return @{ UpdateAll = $true; DirPath = $null }
            }
        }
        
        # Default to update all
        return @{ UpdateAll = $true; DirPath = $null }
    }

    [bool] CheckGitRepository() {
        $gitDir = Join-Path $this.BaseDir '.git'
        return Test-Path $gitDir
    }

    [bool] CheckGitmodules() {
        $gitmodules = Join-Path $this.BaseDir '.gitmodules'
        return Test-Path $gitmodules
    }

    [bool] CheckDirectory([string]$dirPath) {
        $targetDir = Join-Path $this.BaseDir $dirPath
        return Test-Path $targetDir -PathType Container
    }

    [string[]] GetSubmodules() {
        try {
            $result = git -C $this.BaseDir submodule status 2>&1
            if ($LASTEXITCODE -ne 0) {
                return @()
            }
            
            $submodules = @()
            foreach ($line in $result -split "`n") {
                if ($line.Trim()) {
                    $parts = $line -split '\s+'
                    if ($parts.Count -ge 2) {
                        $submodules += $parts[1]
                    }
                }
            }
            
            return $submodules
        } catch {
            return @()
        }
    }

    [object] UpdateSubmodule([string]$submodulePath) {
        try {
            $result = git -C $this.BaseDir submodule update --remote --merge $submodulePath 2>&1
            
            if ($LASTEXITCODE -eq 0) {
                return @{ Success = $true; Error = '' }
            } else {
                return @{ Success = $false; Error = $result }
            }
        } catch {
            return @{ Success = $false; Error = $_.Exception.Message }
        }
    }

    [void] UpdateAllSubmodules() {
        try {
            $result = git -C $this.BaseDir submodule update --remote --merge 2>&1
            
            if ($LASTEXITCODE -eq 0) {
                $outputLines = $result -split "`n"
                foreach ($line in $outputLines) {
                    if ($line.Trim()) {
                        Write-Host "✓ $($line.Trim())"
                    }
                }
                $this.SuccessCount = $outputLines.Count
            } else {
                Write-Host "✗ Error: $result"
                $this.FailureCount = 1
            }
        } catch {
            Write-Host "✗ Error: $($_.Exception.Message)"
            $this.FailureCount = 1
        }
    }

    [bool] Execute([string]$command) {
        $this.StartTime = Get-Date
        $this.SuccessCount = 0
        $this.FailureCount = 0
        
        $parseResult = $this.ParseCommand($command)
        $updateAll = $parseResult.UpdateAll
        $dirPath = $parseResult.DirPath
        
        if (-not $this.CheckGitRepository()) {
            Write-Host "✗ Error: Current directory is not a Git repository"
            return $false
        }
        
        if (-not $this.CheckGitmodules()) {
            Write-Host "✗ Error: No submodules found (.gitmodules file does not exist)"
            return $false
        }
        
        if (-not $updateAll) {
            if (-not $this.CheckDirectory($dirPath)) {
                Write-Host "✗ Error: Specified directory does not exist: $dirPath"
                return $false
            }
        }
        
        if ($updateAll) {
            Write-Host "✓ Starting to update all submodules..."
            $this.UpdateAllSubmodules()
        } else {
            Write-Host "✓ Starting to update submodules in $dirPath..."
            
            $allSubmodules = $this.GetSubmodules()
            $targetSubmodules = $allSubmodules | Where-Object { $_.StartsWith($dirPath) }
            
            if ($targetSubmodules.Count -eq 0) {
                Write-Host "✗ Error: No submodules found in $dirPath directory"
                return $false
            }
            
            foreach ($submodule in $targetSubmodules) {
                Write-Host "✓ Updating: $submodule"
                $updateResult = $this.UpdateSubmodule($submodule)
                $success = $updateResult.Success
                $error = $updateResult.Error
                
                if ($success) {
                    Write-Host "✓ Submodule $submodule updated successfully"
                    $this.SuccessCount++
                } else {
                    Write-Host "✗ Submodule $submodule update failed: $error"
                    $this.FailureCount++
                }
            }
        }
        
        $elapsedTime = (Get-Date) - $this.StartTime
        Write-Host ""
        Write-Host "✓ Submodule update completed"
        Write-Host "✓ Success: $($this.SuccessCount)"
        Write-Host "✗ Failed: $($this.FailureCount)"
        Write-Host "⏱ Total time: $($elapsedTime.TotalSeconds.ToString('F1')) seconds"
        
        return $this.FailureCount -eq 0
    }
}

function Main {
    param (
        [string]$Command
    )
    
    if ([string]::IsNullOrEmpty($Command)) {
        Write-Host "Usage: .\submodule_updater.ps1 <command>"
        Write-Host "Examples:"
        Write-Host "  .\submodule_updater.ps1 '更新所有submodule'"
        Write-Host "  .\submodule_updater.ps1 '更新src/libs下的submodule'"
        exit 1
    }
    
    $updater = New-Object SubmoduleUpdater
    $success = $updater.Execute($Command)
    
    if ($success) {
        exit 0
    } else {
        exit 1
    }
}

if ($MyInvocation.InvocationName -ne '.') {
    $command = $args -join ' '
    Main -Command $command
}
