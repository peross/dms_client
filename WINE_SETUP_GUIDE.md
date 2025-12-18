# Wine Setup Guide for Building Windows Executables

This guide helps you set up Wine to build Windows executables on Linux.

## Step 1: Install Wine (Complete Installation)

Run these commands to install Wine with all necessary components:

```bash
# Add i386 architecture support
sudo dpkg --add-architecture i386

# Update package list
sudo apt-get update

# Install Wine (including 32-bit support)
sudo apt-get install -y wine wine64 wine32:i386
```

## Step 2: Initialize Wine

```bash
# Initialize Wine (this opens a configuration window - just click OK)
winecfg
```

When the configuration window opens, just click OK to close it.

## Step 3: Install Python in Wine

### Option A: Using the Helper Script

```bash
# Make the script executable (if not already)
chmod +x install_python_wine.sh

# Run the installer script
./install_python_wine.sh
```

The script will:
- Download Python installer if needed
- Start the installer in Wine
- Guide you through installation

### Option B: Manual Installation

1. **Download Python installer:**
   ```bash
   wget https://www.python.org/ftp/python/3.10.11/python-3.10.11-amd64.exe
   ```

2. **Run the installer:**
   ```bash
   wine python-3.10.11-amd64.exe
   ```

3. **In the installer window:**
   - ✅ **IMPORTANT:** Check the box "Add Python 3.10 to PATH" at the bottom
   - Click "Install Now"
   - Wait for installation to complete
   - Click "Close" when done

4. **Verify installation:**
   ```bash
   # Find Python
   find ~/.wine/drive_c -name "python.exe"
   
   # Test Python
   wine ~/.wine/drive_c/Python*/python.exe --version
   ```

   You should see something like: `Python 3.10.11`

## Step 4: Build the Windows Executable

Once Python is installed in Wine:

```bash
# Build the executable
./build_windows_wine.sh
```

This will:
- Install PyInstaller and dependencies in Wine
- Convert the icon
- Build the Windows executable
- Output: `dist/DocumentManagementClient.exe`

## Troubleshooting

### Error: "wine32 is missing"

**Solution:**
```bash
sudo dpkg --add-architecture i386
sudo apt-get update
sudo apt-get install wine32:i386
```

### Error: "Python not found in Wine"

**Solution:**
1. Verify Python is installed:
   ```bash
   find ~/.wine/drive_c -name "python.exe"
   ```

2. If not found, reinstall Python (see Step 3)

3. If found but script can't detect it, manually specify:
   ```bash
   PYTHON_WINE=$(find ~/.wine/drive_c -name "python.exe" | head -1)
   wine "$PYTHON_WINE" -m PyInstaller dms_client.spec --clean --noconfirm
   ```

### Error: "Application could not be started"

This usually means Wine needs wine32. Install it:
```bash
sudo apt-get install wine32:i386
```

### Python Installer Fails

**Try these solutions:**

1. **Use 32-bit Python instead:**
   ```bash
   wget https://www.python.org/ftp/python/3.10.11/python-3.10.11.exe
   wine python-3.10.11.exe
   ```

2. **Install winetricks for dependencies:**
   ```bash
   sudo apt-get install winetricks
   winetricks corefonts
   ```

3. **Clean Wine prefix and retry:**
   ```bash
   rm -rf ~/.wine
   winecfg
   wine python-3.10.11-amd64.exe
   ```

### Build Fails with Import Errors

If PyInstaller can't find modules, install them explicitly in Wine:

```bash
PYTHON_WINE=$(find ~/.wine/drive_c -name "python.exe" | head -1)
wine "$PYTHON_WINE" -m pip install PyInstaller Pillow pyinsane2 watchdog PyQt5
```

## Alternative: Simpler Build (Without Full Setup)

If Wine setup is too complex, consider:

1. **Fix GitHub Actions billing** - Add payment method (it's free for public repos)
2. **Use a Windows VM** - If you have a Windows license
3. **Build on a Windows machine** - Friend's computer, etc.

## Quick Verification Checklist

Before building, verify:

- [ ] Wine is installed: `wine --version`
- [ ] wine32 is installed: `dpkg -l | grep wine32`
- [ ] Python is installed in Wine: `find ~/.wine/drive_c -name "python.exe"`
- [ ] Python works: `wine ~/.wine/drive_c/Python*/python.exe --version`
- [ ] You're in the project directory: `pwd`
- [ ] Build script is executable: `ls -l build_windows_wine.sh`

## Expected Output

When build succeeds, you'll see:

```
[SUCCESS] Build complete!
[INFO] Executable: dist/DocumentManagementClient.exe
[INFO] Size: ~150M
```

The executable will be in the `dist/` directory and can be distributed to Windows users (they can run it directly without installation).

