param(
    [ValidateSet("all", "codex", "claude")]
    [string]$Target = "all",
    [switch]$CleanLegacy
)

$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$CodexSkill = Join-Path $Root "dist\codex\paper-spine"
$ClaudeSkills = Join-Path $Root "dist\claude\skills"
$ClaudeCommands = Join-Path $Root "dist\claude\commands"

function Assert-PathExists {
    param([string]$Path)
    if (-not (Test-Path -LiteralPath $Path)) {
        throw "Required path not found: $Path"
    }
}

function Reset-CopyDirectory {
    param(
        [string]$Source,
        [string]$Destination
    )
    Assert-PathExists $Source
    if (Test-Path -LiteralPath $Destination) {
        Remove-Item -LiteralPath $Destination -Recurse -Force
    }
    $parent = Split-Path -Parent $Destination
    New-Item -ItemType Directory -Force -Path $parent | Out-Null
    Copy-Item -LiteralPath $Source -Destination $Destination -Recurse -Force
}

function Remove-IfExists {
    param([string]$Path)
    if (Test-Path -LiteralPath $Path) {
        Remove-Item -LiteralPath $Path -Recurse -Force
    }
}

Assert-PathExists $CodexSkill
Assert-PathExists $ClaudeSkills
Assert-PathExists $ClaudeCommands

if ($Target -eq "all" -or $Target -eq "codex") {
    $codexSkillsDir = Join-Path $HOME ".codex\skills"
    if ($CleanLegacy) {
        Remove-IfExists (Join-Path $codexSkillsDir "PaperSpine")
        Remove-IfExists (Join-Path $codexSkillsDir "PaperSpineV2")
        Remove-IfExists (Join-Path $codexSkillsDir "paper-spine")
    }
    Reset-CopyDirectory $CodexSkill (Join-Path $codexSkillsDir "paper-spine")
    Write-Output "Installed Codex skill: $(Join-Path $codexSkillsDir 'paper-spine')"
}

if ($Target -eq "all" -or $Target -eq "claude") {
    $claudeSkillsDir = Join-Path $HOME ".claude\skills"
    $claudeCommandsDir = Join-Path $HOME ".claude\commands"
    New-Item -ItemType Directory -Force -Path $claudeSkillsDir, $claudeCommandsDir | Out-Null

    if ($CleanLegacy) {
        Remove-IfExists (Join-Path $claudeSkillsDir "PaperSpine")
        Remove-IfExists (Join-Path $claudeSkillsDir "PaperSpineV2")
        Remove-IfExists (Join-Path $claudeSkillsDir "paper-writing-assistant")
        Get-ChildItem -LiteralPath $claudeSkillsDir -Directory -Filter "paper-spine*" -ErrorAction SilentlyContinue |
            Remove-Item -Recurse -Force
        Remove-IfExists (Join-Path $claudeCommandsDir "paperspine.md")
        Remove-IfExists (Join-Path $claudeCommandsDir "paperspine-ui.md")
    }

    Get-ChildItem -LiteralPath $ClaudeSkills -Directory | ForEach-Object {
        Reset-CopyDirectory $_.FullName (Join-Path $claudeSkillsDir $_.Name)
    }
    Get-ChildItem -LiteralPath $ClaudeCommands -File -Filter "*.md" | ForEach-Object {
        Copy-Item -LiteralPath $_.FullName -Destination (Join-Path $claudeCommandsDir $_.Name) -Force
    }
    Write-Output "Installed Claude Code skills: $claudeSkillsDir"
    Write-Output "Installed Claude Code commands: $claudeCommandsDir"
}

Write-Output "PaperSpine install complete. Restart Codex or Claude Code before use."
