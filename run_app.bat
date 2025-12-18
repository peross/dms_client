@echo off
REM Launcher script for Document Management Client (Windows)
REM This script activates the virtual environment and runs the application

REM Get the directory where this batch file is located
cd /d "%~dp0"

REM Check if virtual environment exists
if not exist "venv" (
    echo Error: Virtual environment not found. Please run setup.bat first.
    pause
    exit /b 1
)

REM Activate virtual environment and run the application
call venv\Scripts\activate.bat
python main.py %*

REM Keep window open if there was an error
if errorlevel 1 (
    echo.
    echo Application exited with an error.
    pause
)

