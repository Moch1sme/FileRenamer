param(
    [string]$InstallDir,
    [string]$ExePath,
    [string]$IconPath
)

$ws = New-Object -ComObject WScript.Shell

$desktop = "$env:USERPROFILE\Desktop"
$startmenu = "$env:APPDATA\Microsoft\Windows\Start Menu\Programs"

# Desktop shortcut
$s1 = $ws.CreateShortcut("$desktop\File Renamer.lnk")
$s1.TargetPath = $ExePath
$s1.WorkingDirectory = $InstallDir
$s1.IconLocation = $IconPath
$s1.Description = "File and Folder Renamer"
$s1.Save()

# Start Menu shortcut
$s2 = $ws.CreateShortcut("$startmenu\File Renamer.lnk")
$s2.TargetPath = $ExePath
$s2.WorkingDirectory = $InstallDir
$s2.IconLocation = $IconPath
$s2.Description = "File and Folder Renamer"
$s2.Save()

Write-Host "[OK] Shortcut Desktop dan Start Menu berhasil dibuat."
