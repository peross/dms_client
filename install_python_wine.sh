#!/bin/bash
# Script to install Python in Wine
# Run this before building Windows executables

set -e

echo "========================================"
echo "Installing Python in Wine"
echo "========================================"
echo ""

# Check Wine
if ! command -v wine &> /dev/null; then
    echo "ERROR: Wine is not installed. Please install it first:"
    echo "  sudo apt-get install wine wine64 wine32:i386"
    exit 1
fi

# Download Python installer if not present
PYTHON_INSTALLER="python-3.10.11-amd64.exe"
if [ ! -f "$PYTHON_INSTALLER" ]; then
    echo "Downloading Python installer..."
    wget https://www.python.org/ftp/python/3.10.11/python-3.10.11-amd64.exe
else
    echo "Python installer found: $PYTHON_INSTALLER"
fi

# Set Wine prefix
export WINEPREFIX=~/.wine
export WINEARCH=win64

echo ""
echo "Starting Python installer in Wine..."
echo "IMPORTANT: When the installer opens:"
echo "  1. Check the box 'Add Python 3.10 to PATH'"
echo "  2. Choose 'Install Now'"
echo "  3. Wait for installation to complete"
echo "  4. Click 'Close' when done"
echo ""
echo "Press Enter when ready to start the installer..."
read

# Run the installer
wine "$PYTHON_INSTALLER" /quiet InstallAllUsers=1 PrependPath=1

echo ""
echo "Waiting for installation to complete..."
sleep 5

# Verify installation
PYTHON_WINE=$(find ~/.wine/drive_c -name "python.exe" -type f 2>/dev/null | head -1)

if [ -n "$PYTHON_WINE" ]; then
    echo ""
    echo "SUCCESS! Python installed in Wine:"
    echo "  $PYTHON_WINE"
    echo ""
    echo "Testing Python..."
    wine "$PYTHON_WINE" --version
    echo ""
    echo "You can now run ./build_windows_wine.sh to build the executable."
else
    echo ""
    echo "WARNING: Python installation may have failed."
    echo "Please check if Python is installed manually:"
    echo "  find ~/.wine/drive_c -name 'python.exe'"
    echo ""
    echo "If Python is installed but not found, try:"
    echo "  wine ~/.wine/drive_c/Python*/python.exe --version"
fi

