@echo off
REM Setup script for Document Management Client (Windows)

REM Create virtual environment if it doesn't exist
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

echo Setup complete! To run the application:
echo   venv\Scripts\activate
echo   python main.py

