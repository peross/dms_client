# Document Management Client

A cross-platform Python desktop application for document management with real-time file tracking.

## For End Users - Quick Install

**Want to just install and run? Use the pre-built installers!**

### Windows
1. **Go to the [Releases](https://github.com/YOUR_USERNAME/dms_client/releases) page** (replace `YOUR_USERNAME` with your GitHub username)
2. **Download the latest `DocumentManagementClient-Setup.exe`** installer file
3. **Run the installer** and follow the setup wizard
4. **Launch the application** from Start Menu or Desktop shortcut

**📖 Need help?** See [GITHUB_USER_GUIDE.md](GITHUB_USER_GUIDE.md) for a simple step-by-step guide, or [INSTALLER_GUIDE.md](INSTALLER_GUIDE.md) for detailed instructions.

**Note:** Replace `YOUR_USERNAME` in the GitHub URL with your actual GitHub username, or update the link to point to your repository's releases page.

### Linux
1. **Go to the [Releases](https://github.com/YOUR_USERNAME/dms_client/releases) page** (replace `YOUR_USERNAME` with your GitHub username)
2. **Download the latest `DocumentManagementClient-x86_64.AppImage`** file
3. **Make it executable:** `chmod +x DocumentManagementClient-x86_64.AppImage`
4. **Run it:** `./DocumentManagementClient-x86_64.AppImage`

**See [INSTALLER_GUIDE.md](INSTALLER_GUIDE.md) for detailed installation instructions.**

**Note:** Replace `YOUR_USERNAME` in the GitHub URL with your actual GitHub username.

---

## Creating Releases for Distribution

To create installers and publish them on GitHub for users to download, see [GITHUB_RELEASES.md](GITHUB_RELEASES.md).

---

## For Developers - Building from Source

If you want to modify the code or build your own installers, continue reading below.

## Features

- Select a location to track for document management
- Automatic creation of default folders:
  - General
  - My Folders
  - Shared With Me
- Real-time file monitoring using watchdog
- Multiple view modes:
  - List View: Detailed file information
  - Tree View: Hierarchical folder navigation
  - Grid View: Visual icon-based browsing
- Search/filter functionality
- Cross-platform support (Windows and Linux)

## Requirements

- Python 3.8 or higher
- PyQt5 >= 5.15.0
- watchdog >= 2.1.0
- pyinsane2 >= 2.0.6 (for scanner support)
- Pillow >= 9.0.0 (for image handling)

### System Dependencies (Linux)

On Debian/Ubuntu systems, you need to install:

1. **Python virtual environment support:**
```bash
sudo apt install python3-venv python3-full
```

2. **Qt5 libraries for GUI (required for PyQt5):**
```bash
sudo apt install libxcb-xinerama0 libxcb-cursor0 libxcb-icccm4 libxcb-keysyms1 libxcb-xkb1 libxkbcommon-x11-0
```

Or use the helper script:
```bash
./install_qt_deps.sh
```

3. **Scanner support (optional, for scanning documents):**
```bash
sudo apt install sane sane-utils libsane-dev
```

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for more details on Qt/X11 issues.

## Installation

### Quick Setup (Recommended)

#### Linux/macOS

Simply run the setup script:
```bash
chmod +x setup.sh
./setup.sh
```

The script will:
- Check for Python 3.8+
- Install system dependencies (Qt5 libraries, SANE for scanner support)
- Create a virtual environment
- Install all Python packages
- Create a desktop launcher with icon for easy access

#### Windows

1. **Download the application:**
   - Go to the GitHub repository
   - Click "Code" → "Download ZIP"
   - Extract the ZIP file to a folder (e.g., `C:\Users\YourName\Documents\dms_client`)

2. **Install Python 3.8+** from [python.org](https://www.python.org/downloads/)
   - Make sure to check "Add Python to PATH" during installation

3. **Run setup:**
   - Open Command Prompt (Press `Win + R`, type `cmd`, press Enter)
   - Navigate to the extracted folder:
     ```cmd
     cd C:\Users\YourName\Documents\dms_client
     ```
   - Run the setup script:
     ```cmd
     setup.bat
     ```

The script will:
- Check for Python 3.8+
- Create a virtual environment
- Install all Python packages
- Create a desktop shortcut for easy access

**For detailed step-by-step instructions, see [WINDOWS_INSTALL_GUIDE.md](WINDOWS_INSTALL_GUIDE.md)**

### Manual Installation

If you prefer to install manually or the setup script doesn't work:

#### Linux/macOS

1. Install system dependencies (Ubuntu/Debian):
```bash
sudo apt install python3-venv python3-full
sudo apt install libxcb-xinerama0 libxcb-cursor0 libxcb-icccm4 libxcb-keysyms1 libxcb-xkb1 libxkbcommon-x11-0
sudo apt install sane sane-utils libsane-dev  # For scanner support
```

2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

#### Windows

1. Install Python 3.8+ from [python.org](https://www.python.org/downloads/)
   - Make sure to check "Add Python to PATH" during installation

2. Open Command Prompt or PowerShell and navigate to the project directory

3. Create and activate a virtual environment:
```cmd
python -m venv venv
venv\Scripts\activate
```

4. Install dependencies:
```cmd
pip install -r requirements.txt
```

**See [WINDOWS_INSTALL_GUIDE.md](WINDOWS_INSTALL_GUIDE.md) for detailed step-by-step Windows installation instructions.**

## Usage

After running the setup script, you can launch the application in several ways:

### Easy Way (Recommended)

**Linux/macOS:**
- Double-click "Document Management Client" in your Applications menu, or
- Double-click "dms-client.desktop" on your Desktop

**Windows:**
- Double-click "Document Management Client" on your Desktop, or
- Double-click "run_app.bat" in the application folder

### From Command Line

**Linux/macOS:**
```bash
./run_app.sh
```

**Windows:**
```cmd
run_app.bat
```

### First Run

1. When you first start the application, you'll be prompted to select a location to track
2. Choose a directory where you want to manage your documents
3. The application will automatically create three default folders:
   - General
   - My Folders
   - Shared With Me
4. The selected location will be saved and loaded automatically on subsequent runs

### Using the Application

- **Select Location**: File → Select Location (or Ctrl+O)
- **Scan Document**: File → Scan Document (or Ctrl+Shift+S) or click the 📄 Scan button in toolbar
- **Change View**: View → List View / Tree View / Grid View (or Ctrl+1/2/3)
- **Search Files**: Use the search box to filter files
- **Navigate Folders**: Double-click folders to navigate, use Back/Up buttons to go back
- **Open Files**: Double-click files to open with system default application
- **Exit**: File → Exit (or Ctrl+Q)

### Scanning Documents

1. Connect your scanner to your computer
2. Click the "📄 Scan Document" button or use File → Scan Document
3. Select your scanner from the dropdown (click Refresh if your scanner isn't listed)
4. Configure scan settings (resolution, color mode, format)
5. Click "📄 Scan Document" to start scanning
6. The scanned document will be automatically saved to your current directory (or you can save manually)
7. The file browser will refresh to show your new scanned document

## Configuration

The application stores its configuration in `~/.dms_client/config.json` (Linux) or `%USERPROFILE%\.dms_client\config.json` (Windows).

## Project Structure

```
dms_client/
├── main.py                 # Application entry point
├── ui/                     # UI components
│   ├── main_window.py     # Main window
│   ├── location_dialog.py # Location selection dialog
│   └── file_browser.py    # File browser widget
├── services/              # Background services
│   ├── file_watcher.py    # File monitoring service
│   └── folder_manager.py  # Folder management
├── utils/                 # Utilities
│   └── config.py          # Configuration management
└── requirements.txt       # Dependencies
```

## Updating the Application

See [UPDATE.md](UPDATE.md) for detailed instructions on how to update your installed application.

## Uninstalling the Application

See [UNINSTALL.md](UNINSTALL.md) for instructions on how to remove the application.

## License

This project is provided as-is for educational/personal use.

