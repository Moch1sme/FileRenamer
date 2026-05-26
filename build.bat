@echo off
title Build & Install File Renamer
color 0A
echo.
echo =============================================
echo   INSTALL FILE RENAMER
echo =============================================
echo.

:: Cek Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python tidak ditemukan!
    echo Silakan download Python di: https://www.python.org/downloads/
    echo Pastikan centang "Add Python to PATH" saat install.
    pause
    exit /b 1
)
echo [OK] Python ditemukan.

:: Install dependencies
echo.
echo [1/4] Menginstall dependencies...
pip install pyinstaller pillow --quiet
if errorlevel 1 (
    echo [ERROR] Gagal install dependencies.
    pause
    exit /b 1
)
echo [OK] Dependencies siap.

:: Cek file utama
if not exist "file_renamer.py" (
    echo [ERROR] file_renamer.py tidak ditemukan!
    pause
    exit /b 1
)
if not exist "make_shortcut.ps1" (
    echo [ERROR] make_shortcut.ps1 tidak ditemukan!
    pause
    exit /b 1
)

:: Tentukan icon
set ICON_FLAG=--icon=NONE
if exist "icon.ico" (
    set ICON_FLAG=--icon=icon.ico
    echo [OK] Icon ditemukan.
)

:: Build EXE
echo.
echo [2/4] Membangun EXE (1-2 menit)...
pyinstaller --onefile --windowed --name "FileRenamer" %ICON_FLAG% file_renamer.py
if errorlevel 1 (
    echo [ERROR] Build gagal!
    pause
    exit /b 1
)

:: Install ke folder lokal
set INSTALL_DIR=%LOCALAPPDATA%\FileRenamer
echo.
echo [3/4] Menginstall ke %INSTALL_DIR%...
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"
copy "dist\FileRenamer.exe" "%INSTALL_DIR%\FileRenamer.exe" >nul
if exist "icon.ico" copy "icon.ico" "%INSTALL_DIR%\icon.ico" >nul

:: Cleanup
rmdir /s /q build >nul 2>&1
rmdir /s /q dist >nul 2>&1
del /q FileRenamer.spec >nul 2>&1

:: Buat shortcut via file ps1 terpisah
echo.
echo [4/4] Membuat shortcut Desktop dan Start Menu...
powershell -NoProfile -ExecutionPolicy Bypass -File "make_shortcut.ps1" -InstallDir "%INSTALL_DIR%" -ExePath "%INSTALL_DIR%\FileRenamer.exe" -IconPath "%INSTALL_DIR%\icon.ico"

:: Registry - Windows Search
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\App Paths\FileRenamer.exe" /ve /d "%INSTALL_DIR%\FileRenamer.exe" /f >nul 2>&1
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\App Paths\FileRenamer.exe" /v "Path" /d "%INSTALL_DIR%" /f >nul 2>&1

:: Registry - Add/Remove Programs
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Uninstall\FileRenamer" /v "DisplayName" /d "File Renamer" /f >nul 2>&1
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Uninstall\FileRenamer" /v "DisplayIcon" /d "%INSTALL_DIR%\icon.ico" /f >nul 2>&1
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Uninstall\FileRenamer" /v "UninstallString" /d "%INSTALL_DIR%\uninstall.bat" /f >nul 2>&1
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Uninstall\FileRenamer" /v "InstallLocation" /d "%INSTALL_DIR%" /f >nul 2>&1
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Uninstall\FileRenamer" /v "Publisher" /d "File Renamer App" /f >nul 2>&1
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Uninstall\FileRenamer" /v "NoModify" /t REG_DWORD /d 1 /f >nul 2>&1
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Uninstall\FileRenamer" /v "NoRepair" /t REG_DWORD /d 1 /f >nul 2>&1

:: Buat uninstaller
(
echo @echo off
echo title Uninstall File Renamer
echo set INSTALL_DIR=%%LOCALAPPDATA%%\FileRenamer
echo del /f /q "%%USERPROFILE%%\Desktop\File Renamer.lnk"
echo del /f /q "%%APPDATA%%\Microsoft\Windows\Start Menu\Programs\File Renamer.lnk"
echo reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\App Paths\FileRenamer.exe" /f
echo reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\Uninstall\FileRenamer" /f
echo rmdir /s /q "%%INSTALL_DIR%%"
echo echo File Renamer berhasil dihapus.
echo pause
) > "%INSTALL_DIR%\uninstall.bat"

echo.
echo =============================================
echo   INSTALASI SELESAI!
echo.
echo   - Shortcut ada di Desktop
echo   - Cari "File Renamer" di Start Menu / Search
echo   - Uninstall: %INSTALL_DIR%\uninstall.bat
echo =============================================
echo.
pause
