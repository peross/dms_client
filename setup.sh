#!/bin/bash
# Comprehensive setup script for Document Management Client (Linux)
# This script installs all system dependencies and Python packages

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Document Management Client Setup${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Function to print colored messages
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root (we shouldn't run the whole script as root)
if [ "$EUID" -eq 0 ]; then 
    print_error "Please don't run this script as root. It will ask for sudo when needed."
    exit 1
fi

# Check for Python 3
print_info "Checking for Python 3..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    print_success "Python 3 found: $PYTHON_VERSION"
    
    # Check Python version (need 3.8+)
    PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d'.' -f1)
    PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d'.' -f2)
    if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 8 ]); then
        print_error "Python 3.8 or higher is required. Found: $PYTHON_VERSION"
        exit 1
    fi
else
    print_error "Python 3 is not installed. Please install Python 3.8 or higher."
    echo "  On Ubuntu/Debian: sudo apt install python3 python3-pip"
    exit 1
fi

# Detect Linux distribution
print_info "Detecting Linux distribution..."
if [ -f /etc/os-release ]; then
    . /etc/os-release
    DISTRO=$ID
    print_info "Detected distribution: $DISTRO"
else
    print_warning "Cannot detect Linux distribution. Assuming Debian/Ubuntu."
    DISTRO="ubuntu"
fi

# Install system dependencies
print_info "Checking system dependencies..."

INSTALL_CMD=""
if [[ "$DISTRO" == "ubuntu" || "$DISTRO" == "debian" ]]; then
    INSTALL_CMD="sudo apt install -y"
elif [[ "$DISTRO" == "fedora" || "$DISTRO" == "rhel" || "$DISTRO" == "centos" ]]; then
    INSTALL_CMD="sudo dnf install -y"
elif [[ "$DISTRO" == "arch" || "$DISTRO" == "manjaro" ]]; then
    INSTALL_CMD="sudo pacman -S --noconfirm"
else
    print_warning "Unknown distribution. Please install dependencies manually."
    INSTALL_CMD=""
fi

if [ -n "$INSTALL_CMD" ]; then
    print_info "Installing system dependencies..."
    
    # Check and install python3-venv
    if ! dpkg -l | grep -q python3-venv 2>/dev/null && [[ "$DISTRO" == "ubuntu" || "$DISTRO" == "debian" ]]; then
        print_info "Installing python3-venv..."
        $INSTALL_CMD python3-venv python3-full || print_warning "Failed to install python3-venv. Continuing anyway..."
    fi
    
    # Install Qt5 libraries (needed for PyQt5)
    if [[ "$DISTRO" == "ubuntu" || "$DISTRO" == "debian" ]]; then
        print_info "Installing Qt5 libraries for PyQt5..."
        $INSTALL_CMD libxcb-xinerama0 libxcb-cursor0 libxcb-icccm4 \
                     libxcb-keysyms1 libxcb-xkb1 libxkbcommon-x11-0 \
                     libxcb-render-util0 libxcb-image0 libxcb-randr0 || \
                     print_warning "Some Qt5 libraries may already be installed."
    elif [[ "$DISTRO" == "fedora" || "$DISTRO" == "rhel" || "$DISTRO" == "centos" ]]; then
        print_info "Installing Qt5 libraries for PyQt5..."
        $INSTALL_CMD libxcb xcb-util xcb-util-wm xcb-util-image \
                     xcb-util-keysyms xcb-util-renderutil || \
                     print_warning "Some Qt5 libraries may already be installed."
    fi
    
    # Install SANE for scanner support (optional but recommended)
    print_info "Installing SANE for scanner support..."
    if [[ "$DISTRO" == "ubuntu" || "$DISTRO" == "debian" ]]; then
        $INSTALL_CMD sane sane-utils libsane-dev || print_warning "SANE installation failed. Scanner support may not work."
    elif [[ "$DISTRO" == "fedora" || "$DISTRO" == "rhel" || "$DISTRO" == "centos" ]]; then
        $INSTALL_CMD sane-backends sane-backends-devel || print_warning "SANE installation failed. Scanner support may not work."
    elif [[ "$DISTRO" == "arch" || "$DISTRO" == "manjaro" ]]; then
        $INSTALL_CMD sane sane-airscan || print_warning "SANE installation failed. Scanner support may not work."
    fi
else
    print_warning "Please install the following system dependencies manually:"
    echo "  - python3-venv (or equivalent for your distribution)"
    echo "  - Qt5 libraries (libxcb-xinerama0, libxcb-cursor0, etc.)"
    echo "  - SANE (sane, sane-utils, libsane-dev) for scanner support"
fi

# Create virtual environment
print_info "Setting up Python virtual environment..."
if [ ! -d "venv" ]; then
    print_info "Creating virtual environment..."
    python3 -m venv venv
    print_success "Virtual environment created"
else
    print_info "Virtual environment already exists"
fi

# Activate virtual environment
print_info "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
print_info "Upgrading pip..."
pip install --upgrade pip --quiet

# Install Python dependencies
print_info "Installing Python dependencies from requirements.txt..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    print_success "Python dependencies installed"
else
    print_error "requirements.txt not found!"
    exit 1
fi

# Verify installation
print_info "Verifying installation..."
python3 -c "from PyQt5.QtCore import PYQT_VERSION_STR; print('PyQt5:', PYQT_VERSION_STR)" || {
    print_error "PyQt5 verification failed"
    exit 1
}

python3 -c "import watchdog; print('watchdog: OK')" || {
    print_warning "watchdog verification failed"
}

python3 -c "import pyinsane2; print('pyinsane2: OK')" || {
    print_warning "pyinsane2 verification failed (scanner support may not work)"
}

python3 -c "from PIL import Image; print('Pillow: OK')" || {
    print_warning "Pillow verification failed"
}

# Create desktop launcher
echo ""
print_info "Creating desktop launcher..."
if [ -f "create_launcher.sh" ]; then
    chmod +x create_launcher.sh
    bash create_launcher.sh
else
    print_warning "create_launcher.sh not found. Skipping launcher creation."
fi

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Setup Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "The application is ready to use!"
echo ""
echo "To run the application:"
echo "  Option 1: Double-click 'Document Management Client' in your Applications menu"
echo "  Option 2: Double-click 'dms-client.desktop' on your Desktop"
echo "  Option 3: Run from terminal: ./run_app.sh"
echo ""
echo "Note: Desktop launcher has been created for easy access."
echo ""
