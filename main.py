"""Main application entry point for DMS Client."""
import sys
from pathlib import Path

# Ensure the parent directory is in the path for imports
sys.path.insert(0, str(Path(__file__).parent))

from PyQt5.QtWidgets import QApplication
from ui.main_window import MainWindow


def main():
    """Main function to run the application."""
    app = QApplication(sys.argv)
    app.setApplicationName("Document Management Client")
    app.setOrganizationName("DMS Client")
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    # Run application
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

