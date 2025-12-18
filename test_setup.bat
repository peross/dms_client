@echo off
REM Test script to debug pip upgrade issue
echo Testing pip upgrade...
echo.

python --version
echo.

python -m pip --version
echo.

echo Attempting to upgrade pip...
python -m pip install --upgrade pip
echo.
echo Pip upgrade command completed with errorlevel: %ERRORLEVEL%
echo.

echo Script continues here...
pause

