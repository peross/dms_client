#!/bin/bash
# Script to install all Qt5 dependencies needed for PyQt5

echo "Installing Qt5/X11 dependencies for PyQt5..."

sudo apt install -y \
    libxcb-xinerama0 \
    libxcb-cursor0 \
    libxcb-icccm4 \
    libxcb-keysyms1 \
    libxcb-xkb1 \
    libxkbcommon-x11-0

echo "Done! You can now run the application."

