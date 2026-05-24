@echo off
title Build File Renamer EXE
color 0A
echo.
echo =============================================
echo   BUILD FILE RENAMER - File Renamer App
echo =============================================
echo.

:: Cek Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python tidak ditemukan!
    echo.
    echo Silakan download Python di: https://www.python.org/downloads/
    echo Pastikan centang "Add Python to PATH" saat install.
    pause
    exit /b 1
)

echo [OK] Python ditemukan.

:: Install PyInstaller
echo.
echo [1/3] Menginstall PyInstaller...
pip install pyinstaller --quiet
if errorlevel 1 (
    echo [ERROR] Gagal install PyInstaller.
    pause
    exit /b 1
)
echo [OK] PyInstaller siap.

:: Cek file_renamer.py ada
if not exist "file_renamer.py" (
    echo [ERROR] file_renamer.py tidak ditemukan di folder ini!
    echo Pastikan file_renamer.py dan build.bat ada di folder yang sama.
    pause
    exit /b 1
)

:: Build EXE
echo.
echo [2/3] Membangun file EXE (ini mungkin butuh 1-2 menit)...
pyinstaller --onefile --windowed --name "FileRenamer" --icon=NONE file_renamer.py

if errorlevel 1 (
    echo [ERROR] Build gagal!
    pause
    exit /b 1
)

:: Pindahkan EXE ke folder sekarang
echo.
echo [3/3] Memindahkan FileRenamer.exe...
if exist "dist\FileRenamer.exe" (
    copy "dist\FileRenamer.exe" "FileRenamer.exe" >nul
    echo.
    echo =============================================
    echo   BERHASIL! FileRenamer.exe sudah siap!
    echo   Klik 2x FileRenamer.exe untuk membuka app
echo =============================================
) else (
    echo [ERROR] EXE tidak ditemukan setelah build.
)

:: Cleanup
rmdir /s /q build >nul 2>&1
rmdir /s /q dist >nul 2>&1
del /q FileRenamer.spec >nul 2>&1

echo.
pause
