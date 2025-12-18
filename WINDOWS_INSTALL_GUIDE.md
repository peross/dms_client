# Windows Installation Guide - Step by Step

This guide is for Windows users downloading the application from GitHub.

## Prerequisites

Before installing, you need:

1. **Windows 7 or later** (Windows 10/11 recommended)
2. **Internet connection** (for downloading and installing dependencies)
3. **Administrator privileges** (may be needed for Python installation)

## Step-by-Step Installation

### Step 1: Install Python

1. **Download Python:**
   - Go to [https://www.python.org/downloads/](https://www.python.org/downloads/)
   - Click the big yellow "Download Python" button (it will download the latest version)
   - Or click "Windows" in the menu and download Python 3.8 or newer

2. **Install Python:**
   - Double-click the downloaded installer (e.g., `python-3.x.x.exe`)
   - **IMPORTANT:** Check the box "Add Python to PATH" at the bottom of the installer window
   - Click "Install Now"
   - Wait for installation to complete
   - Click "Close" when done

3. **Verify Python is installed:**
   - Press `Win + R`
   - Type `cmd` and press Enter
   - In the Command Prompt, type:
     ```cmd
     python --version
     ```
   - You should see something like: `Python 3.11.0`
   - If you see "Python is not recognized", Python wasn't added to PATH - reinstall and make sure to check "Add Python to PATH"

### Step 2: Download the Application

1. **Go to the GitHub repository:**
   - Open your web browser
   - Navigate to the GitHub repository URL

2. **Download the application:**
   - Click the green "Code" button (top right)
   - Click "Download ZIP"
   - The file will download (e.g., `dms_client-main.zip`)

3. **Extract the ZIP file:**
   - Find the downloaded ZIP file (usually in your Downloads folder)
   - Right-click on it → "Extract All..."
   - Choose a location (e.g., `C:\Users\YourName\Documents\`)
   - Click "Extract"
   - A folder will be created (e.g., `dms_client-main`)

4. **Rename the folder (optional):**
   - Right-click the extracted folder → "Rename"
   - Change it to `dms_client` (or any name you prefer)

### Step 3: Run Setup

1. **Open Command Prompt:**
   - Press `Win + R`
   - Type `cmd` and press Enter

2. **Navigate to the application folder:**
   ```cmd
   cd C:\Users\YourName\Documents\dms_client-main
   ```
   (Replace with your actual path - if you renamed the folder, use that name)

   **Tip:** You can also:
   - Navigate to the folder in File Explorer
   - Click in the address bar and type `cmd`, then press Enter
   - This opens Command Prompt in that folder automatically

3. **Run the setup script:**
   ```cmd
   setup.bat
   ```

4. **Wait for setup to complete:**
   - The script will:
     - Create a virtual environment
     - Install all required Python packages
     - Create a desktop shortcut
   - This may take a few minutes the first time
   - You'll see messages showing progress

5. **When setup is complete:**
   - You should see "Setup Complete!" message
   - A desktop shortcut "Document Management Client" will be created
   - Press any key to close the setup window

### Step 4: Launch the Application

You have three ways to launch the app:

**Method 1: Desktop Shortcut (Easiest)**
- Double-click "Document Management Client" on your Desktop

**Method 2: Run Script**
- Double-click `run_app.bat` in the application folder

**Method 3: Command Prompt**
```cmd
cd C:\Users\YourName\Documents\dms_client-main
run_app.bat
```

### Step 5: First Run

1. **Select a location to track:**
   - When you first open the app, a dialog will appear
   - Click "Browse" or "Select Location"
   - Choose a folder where you want to manage your documents
   - Click "OK"

2. **Start using the app:**
   - The application will create default folders (General, My Folders, Shared With Me)
   - You can now browse and manage your documents

## Troubleshooting

### "Python is not recognized"

**Problem:** Command Prompt says Python is not found.

**Solution:**
1. Reinstall Python from [python.org](https://www.python.org/downloads/)
2. **Important:** Check "Add Python to PATH" during installation
3. Restart Command Prompt after installation

### "setup.bat is not recognized"

**Problem:** You see an error when running setup.bat.

**Solution:**
1. Make sure you're in the correct folder (the one containing `setup.bat`)
2. Type the full path:
   ```cmd
   C:\Users\YourName\Documents\dms_client-main\setup.bat
   ```

### Setup fails or takes too long

**Problem:** Setup script errors or seems stuck.

**Solution:**
1. Make sure you have internet connection
2. Try running Command Prompt as Administrator:
   - Right-click Command Prompt → "Run as administrator"
   - Navigate to the folder and run setup.bat again
3. Check firewall/antivirus isn't blocking Python or pip

### Application won't start

**Problem:** Double-clicking the shortcut does nothing or shows an error.

**Solution:**
1. Try running from Command Prompt:
   ```cmd
   cd C:\Users\YourName\Documents\dms_client-main
   run_app.bat
   ```
2. Check for error messages - they will tell you what's wrong
3. Make sure Python is installed and in PATH
4. Try running setup.bat again

### "Failed building wheel for pyinsane2"

**Problem:** Setup fails with "Failed building wheel for pyinsane2" error.

**Solution:**
This happens because pyinsane2 needs C++ build tools. See [WINDOWS_SCANNER_FIX.md](WINDOWS_SCANNER_FIX.md) for detailed instructions.

**Quick fix:**
1. Download Visual Studio Build Tools from: https://visualstudio.microsoft.com/downloads/
2. Install "C++ build tools" workload
3. Restart your computer
4. Re-run setup.bat

**Note:** The application will work without scanner support, but scanner functionality will be disabled until you install the build tools.

### Scanner doesn't work

**Problem:** Scanner is not detected or scanning fails.

**Solution:**
1. Make sure pyinsane2 is installed (see above if setup failed)
2. Make sure your scanner is connected and powered on
3. Check Device Manager to ensure Windows recognizes your scanner
4. Install scanner drivers from the manufacturer's website
5. Try using Windows' built-in scanning software first to verify the scanner works

## Updating the Application

If you download a new version from GitHub:

1. **Close the application** if it's running

2. **Download the new ZIP file** and extract it

3. **Copy your configuration** (optional):
   - If you want to keep your settings, copy the config file:
   - From old location: `%USERPROFILE%\.dms_client\config.json`
   - To new location: same path in the new installation

4. **Run setup.bat** in the new folder

5. **Delete the old folder** if you don't need it anymore

## Uninstalling

To remove the application:

1. **Delete the application folder:**
   - Navigate to where you extracted it (e.g., `C:\Users\YourName\Documents\dms_client-main`)
   - Delete the entire folder

2. **Remove desktop shortcut:**
   - Right-click "Document Management Client" on Desktop
   - Click "Delete"

3. **Remove configuration (optional):**
   - Press `Win + R`
   - Type `%USERPROFILE%\.dms_client` and press Enter
   - Delete the folder if it exists

**Note:** Your document files are NOT deleted - they remain in the location you chose to track.

## Need Help?

- Check the main [README.md](README.md) for more information
- Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues
- Review error messages in Command Prompt for specific problems

