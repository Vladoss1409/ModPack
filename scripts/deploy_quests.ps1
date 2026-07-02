# Deploy FTB Quests from repo overrides to local ModPack instance.
$repo = Join-Path $PSScriptRoot "..\overrides\config\ftbquests"
$inst = "$env:APPDATA\.minecraft\versions\ModPack\config\ftbquests"

if (-not (Test-Path $inst)) {
    Write-Error "Instance not found: $inst"
    exit 1
}

$chSrc = Join-Path $repo "quests\chapters"
$chDst = Join-Path $inst "quests\chapters"
New-Item -ItemType Directory -Force -Path $chDst | Out-Null

Get-ChildItem (Join-Path $chDst "*.snbt.snbt") -ErrorAction SilentlyContinue | Remove-Item -Force
Copy-Item -Path (Join-Path $chSrc "*.snbt") -Destination $chDst -Force
Copy-Item -Path (Join-Path $repo "quests\data.snbt") -Destination (Join-Path $inst "quests\data.snbt") -Force
Copy-Item -Path (Join-Path $repo "quests\chapter_groups.snbt") -Destination (Join-Path $inst "quests\chapter_groups.snbt") -Force

Write-Host "Deployed $(@(Get-ChildItem $chDst -Filter '*.snbt').Count) chapters to instance"
