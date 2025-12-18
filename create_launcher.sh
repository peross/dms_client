#!/bin/bash
# Script to create desktop launcher for Document Management Client

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Creating desktop launcher...${NC}"

# Get the absolute path to the project directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
APP_DIR="$SCRIPT_DIR"
ICON_PATH="$APP_DIR/icon.png"
LAUNCHER_SCRIPT="$APP_DIR/run_app.sh"

# Make sure launcher script is executable
chmod +x "$LAUNCHER_SCRIPT"

# Determine Python command (prefer venv if available)
if [ -d "$APP_DIR/venv" ]; then
    PYTHON_CMD="$APP_DIR/venv/bin/python3"
else
    PYTHON_CMD="python3"
fi

# Create icon if it doesn't exist
if [ ! -f "$ICON_PATH" ]; then
    echo "Creating default icon..."
    # Try to create icon using Python/PIL (which we have installed)
    if "$PYTHON_CMD" -c "from PIL import Image" 2>/dev/null; then
        cd "$APP_DIR"
        if [ -f "create_icon.py" ]; then
            "$PYTHON_CMD" create_icon.py "$ICON_PATH"
        else
            # Create icon inline
            "$PYTHON_CMD" << EOF
from PIL import Image, ImageDraw
size = 128
img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)
draw.ellipse([0, 0, size-1, size-1], fill=(33, 150, 243, 255))
margin = size // 4
doc_w = size - 2 * margin
doc_h = size - 2 * margin
draw.rectangle([margin, margin, margin + doc_w, margin + doc_h], fill=(255, 255, 255, 255), outline=(200, 200, 200, 255), width=2)
corner_size = doc_w // 3
draw.polygon([(margin + doc_w - corner_size, margin), (margin + doc_w, margin), (margin + doc_w, margin + corner_size)], fill=(240, 240, 240, 255))
for i in range(1, 4):
    y = margin + doc_h // 3 + i * (doc_h // 8)
    line_w = doc_w - 2 * (doc_w // 6) if i < 3 else doc_w // 2
    draw.rectangle([margin + doc_w // 6, y, margin + doc_w // 6 + line_w, y + 2], fill=(180, 180, 180, 255))
img.save('$ICON_PATH', 'PNG')
EOF
        fi
        cd - > /dev/null
    else
        echo "Note: Could not create icon automatically. Using system default icon."
        ICON_PATH="application-x-executable"
    fi
fi

# Ensure we're in the app directory
cd "$APP_DIR"

# Create .desktop file
DESKTOP_FILE="$HOME/.local/share/applications/dms-client.desktop"

# Determine icon path - use absolute path if file exists, otherwise system icon
if [ -f "$ICON_PATH" ]; then
    ICON_VALUE="$ICON_PATH"
else
    ICON_VALUE="application-x-executable"
fi

cat > "$DESKTOP_FILE" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Document Management Client
Comment=Desktop application for document management with real-time file tracking
Exec="$LAUNCHER_SCRIPT"
Icon=$ICON_VALUE
Terminal=false
Categories=Office;Utility;
StartupNotify=true
EOF

# Make desktop file executable
chmod +x "$DESKTOP_FILE"

# Copy to Desktop if user wants
DESKTOP_DIR="$HOME/Desktop"
if [ -d "$DESKTOP_DIR" ]; then
    cp "$DESKTOP_FILE" "$DESKTOP_DIR/dms-client.desktop"
    chmod +x "$DESKTOP_DIR/dms-client.desktop"
    echo -e "${GREEN}Desktop launcher created on Desktop!${NC}"
fi

echo -e "${GREEN}Launcher created successfully!${NC}"
echo "You can find it in:"
echo "  - Applications menu: Document Management Client"
echo "  - Desktop: dms-client.desktop (if Desktop directory exists)"
echo ""
echo "You can also run the app directly by double-clicking the desktop icon."

