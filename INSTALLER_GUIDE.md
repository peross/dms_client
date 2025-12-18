# Installer Guide for End Users

This guide explains how to install and run the Document Management Client using the pre-built installers.

## Windows Installation

### Option 1: Using the Installer (Recommended)

1. **Download the installer:**
   - Download `DocumentManagementClient-Setup.exe` from the releases page

2. **Run the installer:**
   - Double-click the downloaded `.exe` file
   - If Windows shows a security warning, click "More info" → "Run anyway" (the application is not code-signed)
   - Follow the installation wizard:
     - Choose installation directory (default: `C:\Program Files\Document Management Client`)
     - Select additional options (Desktop shortcut, etc.)
     - Click "Install"

3. **Launch the application:**
   - Double-click the Desktop shortcut, or
   - Open Start Menu → "Document Management Client", or
   - Run from installation directory: `C:\Program Files\Document Management Client\DocumentManagementClient.exe`

4. **Uninstall:**
   - Go to Settings → Apps → Apps & features
   - Find "Document Management Client"
   - Click "Uninstall"

### Option 2: Portable Executable

1. **Download the executable:**
   - Download `DocumentManagementClient.exe` from the releases page

2. **Run the application:**
   - Place the `.exe` file in any folder
   - Double-click to run
   - No installation required!

**Note:** The portable version doesn't create shortcuts or integrate with Windows. It's useful if you want to run the app from a USB drive or without admin rights.

## Linux Installation

### Using AppImage (Recommended)

1. **Download the AppImage:**
   - Download `DocumentManagementClient-x86_64.AppImage` from the releases page

2. **Make it executable:**
   ```bash
   chmod +x DocumentManagementClient-x86_64.AppImage
   ```

3. **Run the application:**
   ```bash
   ./DocumentManagementClient-x86_64.AppImage
   ```

4. **Optional - Create a launcher:**
   - You can move the AppImage to a permanent location (e.g., `~/Applications/`)
   - Create a `.desktop` file or add to your application menu for easier access

**Note:** AppImage is portable - you can run it from anywhere and it doesn't require installation.

### Using Standalone Executable

1. **Download the executable:**
   - Download `DocumentManagementClient` (no extension) from the releases page

2. **Make it executable:**
   ```bash
   chmod +x DocumentManagementClient
   ```

3. **Run the application:**
   ```bash
   ./DocumentManagementClient
   ```

## First Run

When you first start the application:

1. **Select a location to track:**
   - A dialog will appear asking you to select a folder
   - Choose the directory where you want to manage your documents
   - Click "Select"

2. **Default folders are created:**
   - The application automatically creates three folders:
     - **General** - For general documents
     - **My Folders** - Your personal folders
     - **Shared With Me** - Shared documents

3. **Start using the app:**
   - Navigate folders by double-clicking
   - Use the search box to find files
   - Scan documents using the scanner button (if a scanner is connected)

## Scanner Support

### Windows

- **Built-in support:** Windows Image Acquisition (WIA) is built into Windows
- Most USB scanners should work automatically
- If your scanner doesn't work, check Device Manager to ensure it's recognized by Windows

### Linux

- **SANE libraries required:** The application may need SANE (Scanner Access Now Easy) libraries installed
- Install on Ubuntu/Debian:
  ```bash
  sudo apt install sane sane-utils
  ```
- Install on Fedora/RHEL:
  ```bash
  sudo dnf install sane-backends sane-backends-devel
  ```
- After installing, restart the application

**Note:** Scanner functionality is optional. The application will work fine without scanner support - you just won't be able to scan documents.

## Troubleshooting

### Windows

**"Windows protected your PC" warning:**
- This appears because the application is not code-signed
- Click "More info" → "Run anyway"
- The application is safe to use

**Application won't start:**
- Try running as Administrator
- Check if your antivirus is blocking it (add exception if needed)
- Ensure you have enough disk space (100MB+ free)

**Scanner not detected:**
- Ensure scanner is connected and powered on
- Check Device Manager to verify Windows recognizes the scanner
- Try unplugging and replugging the USB cable
- Restart the application

### Linux

**"Permission denied" when running:**
- Make sure the file is executable: `chmod +x DocumentManagementClient-x86_64.AppImage`
- Check file permissions: `ls -l DocumentManagementClient-x86_64.AppImage`

**Application won't start:**
- Try running from terminal to see error messages:
  ```bash
  ./DocumentManagementClient-x86_64.AppImage
  ```
- Check for missing system libraries (Qt5 libraries may be needed)

**Qt/X11 errors:**
- Install Qt5 libraries:
  ```bash
  sudo apt install libxcb-xinerama0 libxcb-cursor0 libxcb-icccm4 libxcb-keysyms1 libxcb-xkb1 libxkbcommon-x11-0
  ```

**Scanner not detected:**
- Install SANE libraries (see Scanner Support section above)
- Ensure your user is in the `scanner` group:
  ```bash
  sudo usermod -a -G scanner $USER
  ```
- Log out and log back in for group changes to take effect
- Restart the application

### General Issues

**Application crashes on startup:**
- Check the console/terminal for error messages
- Try deleting the configuration file:
  - Windows: `%USERPROFILE%\.dms_client\config.json`
  - Linux: `~/.dms_client/config.json`

**Files not showing up:**
- Click "Refresh" button or press F5
- Check if the tracked location still exists
- Try selecting a new location: File → Select Location

## System Requirements

### Windows
- Windows 7 or later (Windows 10/11 recommended)
- 200MB free disk space
- 512MB RAM minimum (1GB recommended)

### Linux
- Any modern Linux distribution (Ubuntu 18.04+, Fedora 30+, etc.)
- 200MB free disk space
- 512MB RAM minimum (1GB recommended)
- X11 or Wayland display server
- Qt5 libraries (for GUI - may need to be installed separately on minimal systems)

## Updating

### Windows (Installer Version)
- Download the new installer
- Run it - it will automatically detect and update the existing installation
- Or uninstall the old version first, then install the new one

### Windows (Portable Version)
- Download the new executable
- Replace the old `DocumentManagementClient.exe` with the new one

### Linux (AppImage)
- Download the new AppImage
- Replace the old AppImage file with the new one
- Make sure it's executable: `chmod +x DocumentManagementClient-x86_64.AppImage`

## Getting Help

If you encounter issues:
1. Check this guide's Troubleshooting section
2. Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for more detailed solutions
3. Check [SCANNER_TROUBLESHOOTING.md](SCANNER_TROUBLESHOOTING.md) for scanner-specific issues
4. Open an issue on GitHub with:
   - Your operating system and version
   - Error messages (if any)
   - Steps to reproduce the problem

