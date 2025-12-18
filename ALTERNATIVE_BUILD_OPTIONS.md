# Alternative Ways to Build Windows Installers (Without GitHub Actions)

If GitHub Actions isn't available due to billing issues, here are alternative methods:

## Option 1: Fix GitHub Actions Billing (If You Want to Use It)

If you just need to add a payment method:

1. Go to GitHub Settings → Billing
2. Add a payment method (GitHub Actions is free for public repos)
3. For private repos, you get 2000 minutes/month free
4. After adding payment method, workflows will work again

**Note:** GitHub Actions is **free for public repositories** with 2000 minutes/month. You only pay if you exceed limits or use private repos extensively.

## Option 2: Use a Different CI/CD Service (Free Alternatives)

### GitLab CI/CD
- Free for public and private repos
- 2000 CI/CD minutes/month
- Similar to GitHub Actions

### GitHub Codespaces (Alternative)
- Free tier available
- Can run Windows builds in cloud

### CircleCI
- Free tier: 6,000 build minutes/month
- Supports Windows builds

## Option 3: Use Wine (Build Locally on Linux)

This lets you build Windows executables directly on Linux using Wine.

### Installation

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y wine wine64 wine32 winetricks

# Initialize Wine (creates ~/.wine)
winecfg
# Click OK in the configuration window
```

### Install Python in Wine

```bash
# Download Python installer
cd /tmp
wget https://www.python.org/ftp/python/3.10.11/python-3.10.11-amd64.exe

# Install Python in Wine
wine python-3.10.11-amd64.exe
# In the installer:
# - Check "Add Python to PATH"
# - Choose "Install Now"
# - Wait for installation
```

### Install Dependencies in Wine

```bash
# Use Wine's Python
wine python.exe -m pip install --upgrade pip
wine python.exe -m pip install PyInstaller Pillow

# Copy your project to Wine's drive
# Wine maps Z: to your Linux root
cp -r /path/to/dms_client ~/.wine/drive_c/dms_client
```

### Build Using Wine

```bash
cd ~/.wine/drive_c/dms_client

# Convert icon (if needed)
wine python.exe build/convert_icon.py icon.png build/windows/icon.ico

# Build executable
wine python.exe -m PyInstaller dms_client.spec --clean --noconfirm

# Find the built executable
# It will be in: ~/.wine/drive_c/dms_client/dist/DocumentManagementClient.exe
```

**Limitations:**
- Inno Setup installer won't work easily in Wine
- You'll get the standalone `.exe` but not the installer
- May have compatibility issues

## Option 4: Use a Windows VM (If Available)

If you have access to a Windows license:

1. **Set up VirtualBox/VMware:**
   ```bash
   # Install VirtualBox
   sudo apt-get install virtualbox
   
   # Download Windows 10/11 ISO
   # Create VM and install Windows
   ```

2. **In the Windows VM:**
   - Install Python 3.10+
   - Copy your project files
   - Run `build_windows.bat`
   - Copy built installer back to Linux

## Option 5: Use Online Windows Services

### GitHub Codespaces with Windows (if available)

### Windows 365 Cloud PC (paid)
- Microsoft's cloud-based Windows
- Can install build tools there

### Remote Windows Machine

If you have access to a Windows computer (friend, colleague, etc.):
1. Copy your project to Windows
2. Run build scripts
3. Get the installer back

## Option 6: Build Just the Executable (Skip Installer)

You can build the standalone `.exe` using Wine, which is simpler:

### Quick Wine Build Script

Create `build_windows_wine.sh`:

```bash
#!/bin/bash
# Build Windows executable using Wine

set -e

echo "Building Windows executable using Wine..."

# Check if Wine is installed
if ! command -v wine &> /dev/null; then
    echo "Wine is not installed. Installing..."
    sudo apt-get update
    sudo apt-get install -y wine wine64
fi

# Check if Python is installed in Wine
if [ ! -f ~/.wine/drive_c/Python*/python.exe ]; then
    echo "Python not found in Wine. Please install it first:"
    echo "  wget https://www.python.org/ftp/python/3.10.11/python-3.10.11-amd64.exe"
    echo "  wine python-3.10.11-amd64.exe"
    exit 1
fi

# Find Python in Wine
PYTHON_WINE=$(find ~/.wine/drive_c/Python* -name "python.exe" | head -1)

# Install dependencies
echo "Installing dependencies in Wine..."
wine "$PYTHON_WINE" -m pip install --upgrade pip
wine "$PYTHON_WINE" -m pip install PyInstaller Pillow -q

# Copy project to Wine drive
PROJECT_DIR="$(pwd)"
WINE_PROJECT="Z:$(echo $PROJECT_DIR | sed 's/\//\\/g')"

# Convert icon
if [ -f "icon.png" ]; then
    echo "Converting icon..."
    wine "$PYTHON_WINE" build/convert_icon.py icon.png build/windows/icon.ico
fi

# Build
echo "Building executable (this may take a few minutes)..."
cd "$PROJECT_DIR"
wine "$PYTHON_WINE" -m PyInstaller dms_client.spec --clean --noconfirm

echo "Build complete!"
echo "Executable location: dist/DocumentManagementClient.exe"
```

Make it executable:
```bash
chmod +x build_windows_wine.sh
./build_windows_wine.sh
```

## Option 7: Use Docker with Windows Container (Advanced)

If you have Docker and Windows container support:

```bash
# Pull Windows container
docker pull mcr.microsoft.com/windows/servercore:ltsc2022

# Build in container
docker run -v $(pwd):C:\app mcr.microsoft.com/windows/servercore:ltsc2022 ...
```

**Note:** This requires Windows containers, which typically need Windows host or special setup.

## Recommended Approach

**If you want the easiest solution:**
1. **Fix GitHub billing** (if it's just missing payment method) - GitHub Actions is free for public repos
2. **Or use Wine** to build the standalone `.exe` (simpler than full installer)
3. **Or use a Windows VM** if you have a Windows license

**For the installer specifically:**
- The installer (`.exe` installer) requires Inno Setup, which is harder in Wine
- The standalone executable (`.exe` without installer) can be built with Wine
- Users can still run the standalone `.exe` directly without installation

## Quick Start: Build Standalone .exe with Wine

1. Install Wine:
   ```bash
   sudo apt-get install wine
   ```

2. Install Python in Wine:
   ```bash
   wget https://www.python.org/ftp/python/3.10.11/python-3.10.11-amd64.exe
   wine python-3.10.11-amd64.exe
   # Check "Add Python to PATH" during installation
   ```

3. Install PyInstaller:
   ```bash
   wine ~/.wine/drive_c/Python*/python.exe -m pip install PyInstaller Pillow
   ```

4. Build:
   ```bash
   # From your project directory
   wine ~/.wine/drive_c/Python*/python.exe -m PyInstaller dms_client.spec --clean --noconfirm
   ```

5. Find your executable:
   ```bash
   ls -lh dist/DocumentManagementClient.exe
   ```

This will create a standalone `.exe` that users can run directly (no installation needed, but also no shortcuts/Start Menu integration).

