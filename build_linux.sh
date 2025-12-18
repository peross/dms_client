#!/bin/bash
# Build script for Linux AppImage
# This script creates a standalone AppImage using PyInstaller

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo "========================================"
echo "Document Management Client - Linux Build"
echo "========================================"
echo ""

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Check for Python
echo -e "${BLUE}[INFO]${NC} Checking for Python 3..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}[ERROR]${NC} Python 3 not found. Please install Python 3.8 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo -e "${GREEN}[SUCCESS]${NC} Python 3 found: $PYTHON_VERSION"

# Check Python version (need 3.8+)
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)
if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 8 ]); then
    echo -e "${RED}[ERROR]${NC} Python 3.8 or higher is required. Found: $PYTHON_VERSION"
    exit 1
fi

# Check for PyInstaller
echo -e "${BLUE}[INFO]${NC} Checking for PyInstaller..."
if ! python3 -c "import PyInstaller" 2>/dev/null; then
    echo -e "${YELLOW}[INFO]${NC} PyInstaller not found. Installing..."
    pip3 install -q PyInstaller>=5.13.0
    if [ $? -ne 0 ]; then
        echo -e "${RED}[ERROR]${NC} Failed to install PyInstaller"
        exit 1
    fi
fi
echo -e "${GREEN}[SUCCESS]${NC} PyInstaller found"

# Check for Pillow (needed for icon conversion)
echo -e "${BLUE}[INFO]${NC} Checking for Pillow..."
if ! python3 -c "from PIL import Image" 2>/dev/null; then
    echo -e "${YELLOW}[INFO]${NC} Pillow not found. Installing..."
    pip3 install -q Pillow
fi

# Create build directories
mkdir -p build/linux
mkdir -p dist

# Copy icon if it exists
if [ -f "icon.png" ]; then
    echo -e "${BLUE}[INFO]${NC} Icon found: icon.png"
    cp icon.png build/linux/icon.png
else
    echo -e "${YELLOW}[WARNING]${NC} icon.png not found. Continuing without icon..."
fi

# Run PyInstaller
echo -e "${BLUE}[INFO]${NC} Running PyInstaller..."
echo "This may take several minutes..."
python3 -m PyInstaller dms_client.spec --clean --noconfirm

if [ $? -ne 0 ]; then
    echo -e "${RED}[ERROR]${NC} PyInstaller failed"
    exit 1
fi

# Check if executable was created
if [ -f "dist/DocumentManagementClient" ]; then
    echo -e "${GREEN}[SUCCESS]${NC} Executable created: dist/DocumentManagementClient"
    
    # Check file size
    SIZE=$(du -h "dist/DocumentManagementClient" | cut -f1)
    echo -e "${BLUE}[INFO]${NC} Executable size: $SIZE"
    
    # Make executable
    chmod +x "dist/DocumentManagementClient"
    
    # Now create AppImage
    echo ""
    echo -e "${BLUE}[INFO]${NC} Creating AppImage..."
    
    # Check for appimagetool
    if command -v appimagetool &> /dev/null; then
        echo -e "${BLUE}[INFO]${NC} appimagetool found, creating AppImage..."
        
        # Create AppDir structure
        APPDIR="build/linux/AppDir"
        rm -rf "$APPDIR"
        mkdir -p "$APPDIR/usr/bin"
        mkdir -p "$APPDIR/usr/share/applications"
        mkdir -p "$APPDIR/usr/share/icons/hicolor/256x256/apps"
        
        # Copy executable
        cp "dist/DocumentManagementClient" "$APPDIR/usr/bin/"
        chmod +x "$APPDIR/usr/bin/DocumentManagementClient"
        
        # Copy icon
        if [ -f "icon.png" ]; then
            cp "icon.png" "$APPDIR/usr/share/icons/hicolor/256x256/apps/dms-client.png"
        fi
        
        # Create .desktop file
        cat > "$APPDIR/usr/share/applications/dms-client.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Document Management Client
Comment=Desktop application for document management with real-time file tracking
Exec=DocumentManagementClient
Icon=dms-client
Categories=Office;Utility;
Terminal=false
StartupNotify=true
EOF
        
        # Create AppRun script
        cat > "$APPDIR/AppRun" << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
exec ./usr/bin/DocumentManagementClient "$@"
EOF
        chmod +x "$APPDIR/AppRun"
        
        # Build AppImage
        appimagetool "$APPDIR" "dist/DocumentManagementClient-x86_64.AppImage" 2>/dev/null
        
        if [ -f "dist/DocumentManagementClient-x86_64.AppImage" ]; then
            chmod +x "dist/DocumentManagementClient-x86_64.AppImage"
            SIZE=$(du -h "dist/DocumentManagementClient-x86_64.AppImage" | cut -f1)
            echo -e "${GREEN}[SUCCESS]${NC} AppImage created: dist/DocumentManagementClient-x86_64.AppImage"
            echo -e "${BLUE}[INFO]${NC} AppImage size: $SIZE"
        else
            echo -e "${YELLOW}[WARNING]${NC} AppImage creation failed. Standalone executable is available."
        fi
    else
        echo -e "${YELLOW}[INFO]${NC} appimagetool not found. Skipping AppImage creation."
        echo -e "${YELLOW}[INFO]${NC} To create AppImage, install appimagetool:"
        echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
        echo "  chmod +x appimagetool-x86_64.AppImage"
        echo "  sudo mv appimagetool-x86_64.AppImage /usr/local/bin/appimagetool"
    fi
else
    echo -e "${RED}[ERROR]${NC} Executable not found in dist directory"
    exit 1
fi

echo ""
echo "========================================"
echo "Build Complete"
echo "========================================"
echo ""
echo "The executable is located at:"
echo "  dist/DocumentManagementClient"
echo ""
if [ -f "dist/DocumentManagementClient-x86_64.AppImage" ]; then
    echo "The AppImage is located at:"
    echo "  dist/DocumentManagementClient-x86_64.AppImage"
    echo ""
fi
echo "You can run the executable directly or distribute the AppImage."
echo ""

