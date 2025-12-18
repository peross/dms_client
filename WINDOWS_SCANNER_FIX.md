# Fixing pyinsane2 Installation on Windows

If you see the error "Failed building wheel for pyinsane2" during setup, this guide will help you fix it.

## Quick Fix (Recommended)

The easiest solution is to install **Visual Studio Build Tools**, which includes the C++ compiler needed to build pyinsane2.

### Step 1: Download Visual Studio Build Tools

1. Go to: https://visualstudio.microsoft.com/downloads/
2. Scroll down to "Tools for Visual Studio"
3. Click "Download" for "Build Tools for Visual Studio"

### Step 2: Install Build Tools

1. Run the downloaded installer (`vs_buildtools.exe`)
2. When the installer opens, check the box for **"C++ build tools"** workload
3. On the right side, make sure these are included:
   - MSVC v143 - VS 2022 C++ x64/x86 build tools
   - Windows 10/11 SDK (latest version)
   - C++ CMake tools for Windows
4. Click "Install"
5. Wait for installation to complete (this may take 10-20 minutes)
6. Restart your computer

### Step 3: Re-run Setup

1. Open Command Prompt
2. Navigate to the application folder
3. Run setup.bat again:
   ```cmd
   setup.bat
   ```

## Alternative Solutions

### Option 1: Install Individual Components

If you don't want to install the full Build Tools, you can install just the essentials:

1. Download **Microsoft C++ Build Tools** from:
   https://visualstudio.microsoft.com/visual-cpp-build-tools/

2. During installation, select:
   - C++ build tools
   - Windows 10/11 SDK

### Option 2: Use Pre-built Wheel (If Available)

Sometimes pre-built wheels are available. Try:

```cmd
pip install --only-binary :all: pyinsane2
```

If this doesn't work, you'll need to install the build tools.

### Option 3: Skip Scanner Support (Temporary)

The application will work without scanner support. You can:

1. Edit `requirements.txt` and comment out the pyinsane2 line:
   ```
   # pyinsane2>=2.0.6
   ```

2. Run setup.bat

3. The app will work, but scanner functionality will be disabled

To enable scanner support later, uncomment the line and install Build Tools, then run:
```cmd
pip install pyinsane2>=2.0.6
```

## Verify Installation

After installing Build Tools and re-running setup, verify pyinsane2 is installed:

```cmd
python -c "import pyinsane2; print('pyinsane2 installed successfully!')"
```

If you see "pyinsane2 installed successfully!", you're good to go!

## Why This Happens

pyinsane2 contains C extensions that need to be compiled from source. Windows doesn't include a C compiler by default, so you need Visual Studio Build Tools to compile it.

This is a one-time setup - once installed, you won't need to do this again.

## Still Having Issues?

1. **Make sure you restarted your computer** after installing Build Tools
2. **Try running Command Prompt as Administrator**:
   - Right-click Command Prompt → "Run as administrator"
   - Navigate to the folder and run setup.bat

3. **Check Python version**:
   ```cmd
   python --version
   ```
   Make sure you're using Python 3.8 or higher

4. **Try installing pyinsane2 manually**:
   ```cmd
   pip install --upgrade pip
   pip install pyinsane2
   ```

