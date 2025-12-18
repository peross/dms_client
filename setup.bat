@echo off
REM Comprehensive setup script for Document Management Client (Windows)
REM This script installs all Python packages and checks for prerequisites

setlocal enabledelayedexpansion

echo ========================================
echo Document Management Client Setup
echo ========================================
echo.

REM Check for Python
echo [INFO] Checking for Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH.
    echo.
    echo Please install Python 3.8 or higher from:
    echo   https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [SUCCESS] Python found: %PYTHON_VERSION%

REM Check Python version (basic check for 3.x)
echo %PYTHON_VERSION% | findstr /R "^3\.[0-9]" >nul
if errorlevel 1 (
    echo %PYTHON_VERSION% | findstr /R "^[4-9]\." >nul
    if errorlevel 1 (
        echo [ERROR] Python 3.8 or higher is required. Found: %PYTHON_VERSION%
        pause
        exit /b 1
    )
)

REM Check for pip
echo [INFO] Checking for pip...
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] pip is not installed. Please install pip.
    pause
    exit /b 1
)
echo [SUCCESS] pip found

REM Create virtual environment
echo [INFO] Setting up Python virtual environment...
if not exist venv (
    echo [INFO] Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment.
        echo This might be because python3-venv is not installed.
        echo Please run: python -m pip install --user virtualenv
        pause
        exit /b 1
    )
    echo [SUCCESS] Virtual environment created
) else (
    echo [INFO] Virtual environment already exists
)

REM Activate virtual environment
echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment.
    echo.
    echo Please check that the venv folder exists and try again.
    pause
    exit /b 1
)

REM Always use venv's Python/pip explicitly to ensure packages install in venv
set PIP_CMD=venv\Scripts\python.exe -m pip
echo [INFO] Using venv Python: venv\Scripts\python.exe

REM Upgrade pip (optional - continue even if it fails)
echo [INFO] Upgrading pip...
echo This may take a moment...
echo.
%PIP_CMD% install --upgrade pip
if errorlevel 1 (
    echo.
    echo [WARNING] pip upgrade had issues, but continuing...
    echo [INFO] This is usually not critical - using existing pip version
    echo.
) else (
    echo.
    echo [SUCCESS] pip upgrade completed
    echo.
)
echo [INFO] Continuing with package installation...
echo.

REM Initialize scanner installed flag
set SCANNER_INSTALLED=0

REM Install Python dependencies
echo [INFO] Installing Python dependencies...
if exist requirements.txt (
    echo [INFO] Installing core dependencies first: PyQt5, watchdog, Pillow
    echo.
    %PIP_CMD% install PyQt5 watchdog Pillow
    if errorlevel 1 (
        echo.
        echo [ERROR] Failed to install core dependencies.
        echo.
        echo Please check your internet connection and try again.
        pause
        exit /b 1
    )
    echo.
    echo [SUCCESS] Core dependencies installed
    
    echo.
    echo [INFO] Installing pyinsane2 for scanner support...
    echo [INFO] Note: This may take a while and may require Visual C++ Build Tools on Windows.
    echo.
    %PIP_CMD% install pyinsane2
    if errorlevel 1 (
        echo.
        echo [WARNING] Failed to install pyinsane2. Scanner support will not be available.
        echo.
        echo [INFO] This is often due to missing Visual C++ Build Tools.
        echo [INFO] To fix this, you can:
        echo   1. Install Visual Studio Build Tools from: https://visualstudio.microsoft.com/downloads/
        echo   2. Select "C++ build tools" workload during installation
        echo   3. Restart your computer
        echo   4. Re-run setup.bat
        echo.
        echo [INFO] The application will still work, but scanner functionality will be disabled.
        echo [INFO] See WINDOWS_SCANNER_FIX.md for detailed instructions.
        echo.
        set SCANNER_INSTALLED=0
    ) else (
        echo [SUCCESS] pyinsane2 installed successfully
        set SCANNER_INSTALLED=1
    )
    echo.
    echo [SUCCESS] Python dependencies installation complete
) else (
    echo [ERROR] requirements.txt not found!
    pause
    exit /b 1
)

REM Verify installation
echo [INFO] Verifying installation...
venv\Scripts\python.exe -c "from PyQt5.QtCore import PYQT_VERSION_STR; print('PyQt5:', PYQT_VERSION_STR)" 2>nul
if errorlevel 1 (
    echo [ERROR] PyQt5 verification failed
    pause
    exit /b 1
)

venv\Scripts\python.exe -c "import watchdog; print('watchdog: OK')" 2>nul
if errorlevel 1 (
    echo [WARNING] watchdog verification failed
)

if "%SCANNER_INSTALLED%"=="1" (
    venv\Scripts\python.exe -c "import pyinsane2; print('pyinsane2: OK')" 2>nul
    if errorlevel 1 (
        echo [WARNING] pyinsane2 verification failed - scanner support may not work
    )
) else (
    echo [INFO] pyinsane2: Not installed (scanner support disabled)
)

venv\Scripts\python.exe -c "from PIL import Image; print('Pillow: OK')" 2>nul
if errorlevel 1 (
    echo [WARNING] Pillow verification failed
)

REM Create desktop shortcut
echo.
echo [INFO] Creating desktop shortcut...
if exist run_app.bat (
    REM Create a VBS script to create the shortcut
    set SHORTCUT_PATH=%USERPROFILE%\Desktop\Document Management Client.lnk
    set TARGET_PATH=%CD%\run_app.bat
    set ICON_PATH=%SystemRoot%\System32\imageres.dll,3
    
    echo Set oWS = WScript.CreateObject("WScript.Shell") > CreateShortcut.vbs
    echo sLinkFile = "%SHORTCUT_PATH%" >> CreateShortcut.vbs
    echo Set oLink = oWS.CreateShortcut(sLinkFile) >> CreateShortcut.vbs
    echo oLink.TargetPath = "%TARGET_PATH%" >> CreateShortcut.vbs
    echo oLink.WorkingDirectory = "%CD%" >> CreateShortcut.vbs
    echo oLink.IconLocation = "%ICON_PATH%" >> CreateShortcut.vbs
    echo oLink.Description = "Document Management Client" >> CreateShortcut.vbs
    echo oLink.Save >> CreateShortcut.vbs
    
    cscript //nologo CreateShortcut.vbs >nul 2>&1
    del CreateShortcut.vbs >nul 2>&1
    
    if exist "%SHORTCUT_PATH%" (
        echo [SUCCESS] Desktop shortcut created!
    ) else (
        echo [WARNING] Could not create desktop shortcut automatically.
        echo You can create it manually by right-clicking run_app.bat and selecting "Create shortcut"
    )
) else (
    echo [WARNING] run_app.bat not found. Skipping shortcut creation.
)

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo The application is ready to use!
echo.
echo To run the application:
echo   Option 1: Double-click "Document Management Client" on your Desktop
echo   Option 2: Double-click run_app.bat in the application folder
echo   Option 3: Run from Command Prompt: run_app.bat
echo.
echo NOTE: For scanner support on Windows:
echo   - WIA (Windows Image Acquisition) is usually already available
echo   - If your scanner doesn't work, make sure Windows Scanner drivers are installed
echo   - Check Device Manager to ensure your scanner is recognized
echo.

pause
