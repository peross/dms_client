#!/bin/bash
# Build Windows executable using Wine (simplified version)
# This builds the standalone .exe file (not the installer)

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo "========================================"
echo "Building Windows Executable with Wine"
echo "========================================"
echo ""

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Check if Wine is installed
if ! command -v wine &> /dev/null; then
    echo -e "${YELLOW}[INFO]${NC} Wine is not installed."
    echo "Installing Wine..."
    sudo apt-get update
    sudo apt-get install -y wine wine64 wine32:i386
fi

# Check if wine32 is installed
if ! dpkg -l | grep -q "wine32.*i386"; then
    echo -e "${YELLOW}[INFO]${NC} wine32:i386 is missing. Installing..."
    sudo dpkg --add-architecture i386
    sudo apt-get update
    sudo apt-get install -y wine32:i386
fi

# Check if Wine is initialized
if [ ! -d ~/.wine ]; then
    echo -e "${YELLOW}[INFO]${NC} Initializing Wine..."
    WINEPREFIX=~/.wine winecfg
    echo "Wine initialized."
fi

# Try to fix Wine if it's broken
echo -e "${BLUE}[INFO]${NC} Checking Wine installation..."
if ! wine --version &>/dev/null; then
    echo -e "${YELLOW}[INFO]${NC} Wine may need reconfiguration. Running winecfg..."
    WINEPREFIX=~/.wine winecfg
fi

# Find Python in Wine (exclude venv and scripts directories)
# Try common locations first
if [ -f ~/.wine/drive_c/Program\ Files/Python*/python.exe ]; then
    PYTHON_WINE=$(find ~/.wine/drive_c/Program\ Files/Python* -maxdepth 1 -name "python.exe" -type f 2>/dev/null | head -1)
elif [ -f ~/.wine/drive_c/Python*/python.exe ]; then
    PYTHON_WINE=$(find ~/.wine/drive_c/Python* -maxdepth 1 -name "python.exe" -type f 2>/dev/null | head -1)
else
    # Search but exclude venv directories
    PYTHON_WINE=$(find ~/.wine/drive_c -name "python.exe" -type f 2>/dev/null | grep -v "/venv/" | grep -v "/Scripts/" | head -1)
fi

if [ -z "$PYTHON_WINE" ]; then
    echo -e "${RED}[ERROR]${NC} Python not found in Wine."
    echo ""
    echo "Please install Python in Wine:"
    echo "  1. Download: wget https://www.python.org/ftp/python/3.10.11/python-3.10.11-amd64.exe"
    echo "  2. Install: wine python-3.10.11-amd64.exe"
    echo "  3. Make sure to check 'Add Python to PATH' during installation"
    exit 1
fi

echo -e "${GREEN}[SUCCESS]${NC} Found Python in Wine: $PYTHON_WINE"

# Install/upgrade pip
echo -e "${BLUE}[INFO]${NC} Upgrading pip..."
wine "$PYTHON_WINE" -m pip install --upgrade pip -q

# Install dependencies
echo -e "${BLUE}[INFO]${NC} Installing PyInstaller and Pillow..."
wine "$PYTHON_WINE" -m pip install PyInstaller Pillow -q

# Convert icon if it exists
if [ -f "icon.png" ]; then
    echo -e "${BLUE}[INFO]${NC} Converting icon..."
    if [ -f "build/convert_icon.py" ]; then
        wine "$PYTHON_WINE" build/convert_icon.py icon.png build/windows/icon.ico || echo "Icon conversion failed, continuing..."
    fi
else
    echo -e "${YELLOW}[WARNING]${NC} icon.png not found, skipping icon conversion"
fi

# Build executable
echo -e "${BLUE}[INFO]${NC} Building executable (this may take several minutes)..."
wine "$PYTHON_WINE" -m PyInstaller dms_client.spec --clean --noconfirm

# Check result
if [ -f "dist/DocumentManagementClient.exe" ]; then
    SIZE=$(du -h "dist/DocumentManagementClient.exe" | cut -f1)
    echo ""
    echo -e "${GREEN}[SUCCESS]${NC} Build complete!"
    echo -e "${BLUE}[INFO]${NC} Executable: dist/DocumentManagementClient.exe"
    echo -e "${BLUE}[INFO]${NC} Size: $SIZE"
    echo ""
    echo "Note: This is a standalone executable. Users can run it directly"
    echo "without installation. For a full installer with shortcuts, you'll"
    echo "need to build on a Windows machine or use GitHub Actions."
else
    echo -e "${RED}[ERROR]${NC} Build failed - executable not found"
    exit 1
fi

