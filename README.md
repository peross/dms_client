# Document Management Client

A cross-platform Python desktop application for document management with real-time file tracking.

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

### Linux/macOS

1. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

Or use the setup script:
```bash
chmod +x setup.sh
./setup.sh
```

### Windows

1. **Install Python 3.8+** from [python.org](https://www.python.org/downloads/)
   - Make sure to check "Add Python to PATH" during installation

2. Open Command Prompt or PowerShell and navigate to the project directory:
```cmd
cd C:\path\to\dms_client
```

3. Create and activate a virtual environment:
```cmd
python -m venv venv
venv\Scripts\activate
```

4. Install dependencies:
```cmd
pip install -r requirements.txt
```

Or use the setup script:
```cmd
setup.bat
```

**See [WINDOWS_SETUP.md](WINDOWS_SETUP.md) for detailed Windows setup instructions.**

## Usage

### Linux/macOS

1. Activate the virtual environment (if not already active):
```bash
source venv/bin/activate
```

2. Run the application:
```bash
python main.py
```

### Windows

1. Activate the virtual environment (if not already active):
```cmd
venv\Scripts\activate
```

2. Run the application:
```cmd
python main.py
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

## License

This project is provided as-is for educational/personal use.

