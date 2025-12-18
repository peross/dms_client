# Windows Setup Guide

This guide will help you set up and run the Document Management Client on Windows.

## Quick Start (Recommended)

If you downloaded the app from GitHub:

1. **Download Python 3.8+** from [python.org](https://www.python.org/downloads/)
   - Make sure to check "Add Python to PATH" during installation

2. **Download the application**
   - Go to the GitHub repository
   - Click the green "Code" button → "Download ZIP"
   - Extract the ZIP file to a folder (e.g., `C:\Users\YourName\Documents\dms_client`)

3. **Run the setup script**
   - Open Command Prompt (Press `Win + R`, type `cmd`, press Enter)
   - Navigate to the application folder:
     ```cmd
     cd C:\Users\YourName\Documents\dms_client
     ```
   - Run the setup:
     ```cmd
     setup.bat
     ```

4. **Launch the application**
   - Double-click "Document Management Client" on your Desktop, or
   - Double-click `run_app.bat` in the application folder

That's it! The setup script does everything for you.

## Prerequisites

1. **Python 3.8 or higher**
   - Download from [python.org](https://www.python.org/downloads/)
   - During installation, check "Add Python to PATH"
   - Verify installation: Open Command Prompt and run `python --version`

2. **Git** (optional, if cloning from repository)
   - Download from [git-scm.com](https://git-scm.com/download/win)

## Installation Steps

### 1. Open Command Prompt or PowerShell

- Press `Win + R`, type `cmd` and press Enter, OR
- Press `Win + X` and select "Windows PowerShell" or "Terminal"

### 2. Navigate to the Project Directory

```cmd
cd C:\path\to\dms_client
```

Replace `C:\path\to\dms_client` with the actual path where you have the project.

### 3. Create Virtual Environment

```cmd
python -m venv venv
```

This creates a virtual environment in a folder named `venv`.

### 4. Activate Virtual Environment

```cmd
venv\Scripts\activate
```

You should see `(venv)` at the beginning of your command prompt.

**Note:** If you get an execution policy error in PowerShell, run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 5. Install Dependencies

```cmd
pip install -r requirements.txt
```

This will install:
- PyQt5 (GUI framework)
- watchdog (file monitoring)
- pyinsane2 (scanner support)
- Pillow (image handling)

### 6. (Optional) Install Scanner Support

For scanner functionality on Windows:
- Most scanners should work with Windows Image Acquisition (WIA) which is built into Windows
- No additional system packages needed - pyinsane2 will use WIA automatically
- If you have issues, ensure your scanner drivers are installed

## Running the Application

### Method 1: Command Line

1. Make sure virtual environment is activated (you should see `(venv)` in prompt)
2. Navigate to project directory
3. Run:
```cmd
python main.py
```

### Method 2: Create a Desktop Shortcut

1. Right-click on desktop → New → Shortcut
2. Enter the target:
```
C:\path\to\python.exe C:\path\to\dms_client\main.py
```
   Replace paths with your actual Python and project paths
3. For the virtual environment, create a batch file instead:

**Create `run_dms_client.bat` in the project directory:**
```batch
@echo off
cd /d "%~dp0"
call venv\Scripts\activate
python main.py
pause
```

Then create a shortcut to this `.bat` file.

## Troubleshooting

### Python Not Found

If `python` command doesn't work, try:
- `python3`
- `py` (Python launcher)
- Reinstall Python and check "Add Python to PATH"

### PyQt5 Issues

If you see errors about missing DLLs:
1. Install Visual C++ Redistributable:
   - Download from [Microsoft](https://aka.ms/vs/17/release/vc_redist.x64.exe)
   - Install and restart

### Scanner Not Detected

1. Ensure scanner is connected and powered on
2. Install scanner drivers from manufacturer's website
3. Test scanner in Windows Settings → Devices → Printers & scanners
4. In the app, click "Refresh" in the scanner dialog

### Application Won't Start

1. Check Python version: `python --version` (should be 3.8+)
2. Verify virtual environment is activated
3. Reinstall dependencies: `pip install --upgrade -r requirements.txt`
4. Check for error messages in the command window

## Quick Start Checklist

- [ ] Python 3.8+ installed
- [ ] Python added to PATH
- [ ] Virtual environment created (`python -m venv venv`)
- [ ] Virtual environment activated (`venv\Scripts\activate`)
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Application runs (`python main.py`)

## Uninstalling

To remove the application:
1. Delete the project folder
2. (Optional) Delete virtual environment folder `venv`

No system-wide changes are made, so no additional cleanup needed.

