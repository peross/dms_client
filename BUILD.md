# Building Installers

This document describes how to build standalone installers for the Document Management Client application.

## Prerequisites

### For Windows Builds

- **Python 3.8+** installed and in PATH
- **PyInstaller 5.13.0+** (will be installed automatically by build script)
- **Pillow** (for icon conversion, will be installed automatically)
- **Inno Setup 5 or 6** (for creating installer .exe)
  - Download from: https://jrsoftware.org/isdl.php
  - Not required if you only need the standalone executable

### For Linux Builds

- **Python 3.8+** installed
- **PyInstaller 5.13.0+** (will be installed automatically by build script)
- **Pillow** (for icon handling, will be installed automatically)
- **appimagetool** (optional, for creating AppImage)
  - Download from: https://github.com/AppImage/AppImageKit/releases
  - Or install: `wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage && chmod +x appimagetool-x86_64.AppImage && sudo mv appimagetool-x86_64.AppImage /usr/local/bin/appimagetool`

## Building Windows Installer

### Step 1: Build the Executable

1. Open Command Prompt or PowerShell
2. Navigate to the project directory:
   ```cmd
   cd path\to\dms_client
   ```
3. Run the build script:
   ```cmd
   build_windows.bat
   ```

This will:
- Check for Python and required tools
- Convert `icon.png` to `icon.ico` for Windows
- Run PyInstaller to create `dist\DocumentManagementClient.exe`
- The executable will be a standalone file (100-200MB, includes Python and all dependencies)

### Step 2: Create the Installer (Optional)

If you want to create a proper installer (.exe installer), you need Inno Setup:

1. Install Inno Setup from https://jrsoftware.org/isdl.php
2. Run the installer build script:
   ```cmd
   build\windows\build_installer.bat
   ```

This will create `dist\DocumentManagementClient-Setup.exe`, which:
- Installs the application to `Program Files\Document Management Client`
- Creates Start Menu shortcuts
- Optionally creates Desktop shortcut
- Includes uninstaller
- Handles proper Windows integration

### Manual Installer Creation

Alternatively, you can open `build\windows\installer.iss` in Inno Setup Compiler and build it manually.

## Building Linux AppImage

### Step 1: Build the Executable and AppImage

1. Open Terminal
2. Navigate to the project directory:
   ```bash
   cd path/to/dms_client
   ```
3. Make the build script executable (if not already):
   ```bash
   chmod +x build_linux.sh
   ```
4. Run the build script:
   ```bash
   ./build_linux.sh
   ```

This will:
- Check for Python and required tools
- Run PyInstaller to create `dist/DocumentManagementClient`
- Create AppImage structure (if appimagetool is available)
- Generate `dist/DocumentManagementClient-x86_64.AppImage`

The AppImage is a single-file portable executable that:
- Can be run on most Linux distributions
- Doesn't require installation
- Includes all dependencies
- Can be made executable: `chmod +x DocumentManagementClient-x86_64.AppImage`

### Distribution

Users can simply:
1. Download the AppImage
2. Make it executable: `chmod +x DocumentManagementClient-x86_64.AppImage`
3. Run it: `./DocumentManagementClient-x86_64.AppImage`

## Build Artifacts

After building, you'll find:

- **Windows:**
  - `dist/DocumentManagementClient.exe` - Standalone executable
  - `dist/DocumentManagementClient-Setup.exe` - Installer (if created)
  - `build/windows/icon.ico` - Converted icon file

- **Linux:**
  - `dist/DocumentManagementClient` - Standalone executable
  - `dist/DocumentManagementClient-x86_64.AppImage` - AppImage (if appimagetool available)
  - `build/linux/` - Build artifacts

## Troubleshooting

### PyInstaller Issues

**Import errors in the built executable:**
- Check `dms_client.spec` for missing `hiddenimports`
- Test the executable and add any missing modules to `hiddenimports`

**Large file size:**
- This is normal (100-200MB) - PyInstaller bundles Python interpreter and all dependencies
- UPX compression is enabled in the spec file to reduce size

**Scanner not working:**
- pyinsane2 may require system libraries that aren't bundled
- On Windows: WIA (Windows Image Acquisition) is built into Windows
- On Linux: Users may need to install SANE libraries separately

### Windows-Specific Issues

**"Python not found":**
- Ensure Python is installed and in PATH
- Try using `py` command instead of `python`

**Icon conversion fails:**
- Ensure Pillow is installed: `pip install Pillow`
- Check that `icon.png` exists in the project root

**Inno Setup not found:**
- Install Inno Setup from the official website
- Or build the installer manually using Inno Setup Compiler

### Linux-Specific Issues

**AppImage creation fails:**
- Ensure appimagetool is installed and in PATH
- AppImage creation is optional - the standalone executable will still work

**Executable won't run:**
- Make sure it's executable: `chmod +x dist/DocumentManagementClient`
- Check for missing system libraries (Qt5 libraries may still be needed)
- Test on a clean system to identify missing dependencies

**Qt/X11 errors:**
- Some Qt libraries may still need to be installed on the target system
- See TROUBLESHOOTING.md for Qt-related issues

## Testing

Before distributing:

1. **Test on clean system:**
   - Windows: Test on a VM without Python installed
   - Linux: Test on a minimal Linux installation or different distribution

2. **Test all features:**
   - File browsing and navigation
   - Scanner functionality (if applicable)
   - File watching
   - All menu items and dialogs

3. **Test scanner:**
   - Verify scanner detection works
   - Test scanning documents
   - Verify scanned files are saved correctly

## Customization

### Changing Application Name

1. Edit `dms_client.spec`:
   - Change `name='DocumentManagementClient'` to your desired name

2. Edit build scripts:
   - Update references to executable name
   - Update installer scripts

### Changing Icon

1. Replace `icon.png` in the project root
2. Rebuild - the icon will be automatically converted and used

### Version Information

Edit `build/windows/installer.iss` to update:
- `MyAppVersion` - Application version
- `MyAppPublisher` - Publisher name
- `AppId` - Unique application ID (generate new GUID if needed)

## Distribution

### Recommended Approach

1. **Create releases on GitHub:**
   - Create a new release tag
   - Upload both Windows installer and Linux AppImage
   - Add release notes

2. **File sizes:**
   - Windows installer: ~100-200MB
   - Linux AppImage: ~100-200MB
   - These sizes are normal due to bundled Python interpreter

3. **Naming convention:**
   - Windows: `DocumentManagementClient-Setup-v1.0.0.exe`
   - Linux: `DocumentManagementClient-x86_64-v1.0.0.AppImage`

