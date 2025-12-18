# How to Uninstall the Application

## Complete Removal (Recommended)

### Step 1: Remove Desktop Launcher

**Linux/macOS:**
```bash
rm ~/.local/share/applications/dms-client.desktop
rm ~/Desktop/dms-client.desktop
```

**Windows:**
- Right-click on the desktop shortcut "Document Management Client"
- Select "Delete"

### Step 2: Remove Application Directory

**Linux/macOS:**
```bash
rm -rf /path/to/dms_client
```

For example, if it's in your Documents:
```bash
rm -rf ~/Documents/Racunari/dms_client
```

**Windows:**
- Navigate to the application folder (e.g., `C:\path\to\dms_client`)
- Delete the entire folder

### Step 3: (Optional) Remove Configuration Files

The application stores configuration in:

**Linux/macOS:**
```bash
rm -rf ~/.dms_client
```

**Windows:**
```
Delete: %USERPROFILE%\.dms_client
```

### Step 4: (Optional) Remove System Dependencies

⚠️ **Warning:** Only do this if you're sure no other applications use these packages!

**Linux (Ubuntu/Debian):**
```bash
# Qt5 libraries (only if not used by other apps)
sudo apt remove libxcb-xinerama0 libxcb-cursor0 libxcb-icccm4 libxcb-keysyms1 libxcb-xkb1 libxkbcommon-x11-0 libxcb-render-util0 libxcb-image0 libxcb-randr0

# SANE scanner support (only if not used by other apps)
sudo apt remove sane sane-utils libsane-dev
```

**Windows:**
- No system dependencies were installed - Python packages are in the venv folder which gets deleted with the application

---

## Quick Removal Script

You can create a simple script to remove everything:

**Linux/macOS** (`uninstall.sh`):
```bash
#!/bin/bash

echo "Uninstalling Document Management Client..."

# Remove desktop launcher
rm -f ~/.local/share/applications/dms-client.desktop
rm -f ~/Desktop/dms-client.desktop

# Remove configuration
read -p "Remove configuration files? (~/.dms_client) [y/N]: " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    rm -rf ~/.dms_client
    echo "Configuration removed."
fi

# Remove application directory
read -p "Remove application directory? ($(pwd)) [y/N]: " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    cd ..
    rm -rf "$(basename $(pwd))"
    echo "Application directory removed."
fi

echo "Uninstallation complete!"
```

**Windows** (`uninstall.bat`):
```batch
@echo off
echo Uninstalling Document Management Client...

REM Remove desktop shortcut
del "%USERPROFILE%\Desktop\Document Management Client.lnk" 2>nul

REM Remove configuration
set /p CONFIG="Remove configuration files? (%USERPROFILE%\.dms_client) [y/N]: "
if /i "%CONFIG%"=="y" (
    rd /s /q "%USERPROFILE%\.dms_client"
    echo Configuration removed.
)

REM Remove application directory
set /p APPDIR="Remove application directory? (%CD%) [y/N]: "
if /i "%APPDIR%"=="y" (
    cd ..
    rd /s /q "dms_client"
    echo Application directory removed.
)

echo Uninstallation complete!
pause
```

---

## What Gets Removed

✅ **Removed:**
- Application directory (including virtual environment)
- Desktop launcher/shortcut
- Application menu entry
- Configuration files (if you choose to remove them)

❌ **Not Removed (by default):**
- System dependencies (Qt5 libraries, SANE) - kept in case other apps need them
- Python itself (if installed system-wide)

---

## Notes

- The virtual environment (`venv/`) is completely self-contained and will be removed with the application directory
- Your document files are NOT removed - they're stored in the location you chose to track
- Configuration removal is optional - it contains your tracked location preference

