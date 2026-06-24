# Sync overrides to instance "Moj mod pak"
# Run: powershell -ExecutionPolicy Bypass -File scripts/sync_to_instance.ps1

$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $PSScriptRoot
$Instance = Join-Path $env:APPDATA '.minecraft\versions\Мой мод пак'

if (-not (Test-Path $Instance)) {
    Write-Error "Instance not found: $Instance"
}

Write-Host "CoopTech sync -> $Instance"

$QuestSrc = Join-Path $Root 'overrides\config\ftbquests'
$QuestDst = Join-Path $Instance 'config\ftbquests'
if (Test-Path $QuestDst) { Remove-Item $QuestDst -Recurse -Force }
Copy-Item $QuestSrc $QuestDst -Recurse -Force
Write-Host '  config/ftbquests/ replaced'

$KubeSrc = Join-Path $Root 'overrides\kubejs'
$KubeDst = Join-Path $Instance 'kubejs'
Copy-Item $KubeSrc $KubeDst -Recurse -Force
Write-Host '  kubejs/ copied'

$DefSrc = Join-Path $Root 'overrides\defaultconfigs'
if (Test-Path $DefSrc) {
    $DefDst = Join-Path $Instance 'defaultconfigs'
    Copy-Item $DefSrc $DefDst -Recurse -Force
    Write-Host '  defaultconfigs/ copied'
}

Write-Host ''
Write-Host 'Done. Full client restart required.'
Write-Host 'Do NOT save quests in FTB Editing Mode - it corrupts item tasks to air.'
