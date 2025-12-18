@echo off
REM Build script for Windows executable and installer
REM This script creates a standalone executable using PyInstaller
REM and optionally creates an installer using Inno Setup

setlocal enabledelayedexpansion

echo ========================================
echo Document Management Client - Windows Build
echo ========================================
echo.

REM Get the script directory
set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

REM Check for Python
echo [INFO] Checking for Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [SUCCESS] Python found: %PYTHON_VERSION%

REM Check for PyInstaller
echo [INFO] Checking for PyInstaller...
python -c "import PyInstaller" >nul 2>&1
if errorlevel 1 (
    echo [INFO] PyInstaller not found. Installing...
    python -m pip install -q PyInstaller>=5.13.0
    if errorlevel 1 (
        echo [ERROR] Failed to install PyInstaller
        pause
        exit /b 1
    )
)
echo [SUCCESS] PyInstaller found

REM Check for Pillow (needed for icon conversion)
echo [INFO] Checking for Pillow...
python -c "from PIL import Image" >nul 2>&1
if errorlevel 1 (
    echo [INFO] Pillow not found. Installing...
    python -m pip install -q Pillow
    if errorlevel 1 (
        echo [WARNING] Failed to install Pillow. Icon conversion may fail.
    )
)

REM Create build directories
if not exist "build\windows" mkdir "build\windows"
if not exist "dist" mkdir "dist"

REM Convert icon PNG to ICO
echo [INFO] Converting icon.png to icon.ico...
if exist "icon.png" (
    python build\convert_icon.py icon.png build\windows\icon.ico
    if errorlevel 1 (
        echo [WARNING] Icon conversion failed. Continuing without icon...
    ) else (
        echo [SUCCESS] Icon converted
    )
) else (
    echo [WARNING] icon.png not found. Continuing without icon...
)

REM Run PyInstaller
echo [INFO] Running PyInstaller...
echo This may take several minutes...
python -m PyInstaller dms_client.spec --clean --noconfirm
if errorlevel 1 (
    echo [ERROR] PyInstaller failed
    pause
    exit /b 1
)

REM Check if executable was created
if exist "dist\DocumentManagementClient.exe" (
    echo [SUCCESS] Executable created: dist\DocumentManagementClient.exe
    
    REM Check file size
    for %%A in ("dist\DocumentManagementClient.exe") do set SIZE=%%~zA
    set /a SIZE_MB=!SIZE! / 1048576
    echo [INFO] Executable size: !SIZE_MB! MB
) else (
    echo [ERROR] Executable not found in dist directory
    pause
    exit /b 1
)

echo.
echo ========================================
echo Build Complete
echo ========================================
echo.
echo The executable is located at:
echo   dist\DocumentManagementClient.exe
echo.
echo To create an installer, you need Inno Setup installed and run:
echo   build\windows\installer.iss
echo.
echo Or use the build installer script if available.
echo.
pause

