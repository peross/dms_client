"""Main application entry point for DMS Client."""
import sys
import traceback
from pathlib import Path

# Ensure the parent directory is in the path for imports
sys.path.insert(0, str(Path(__file__).parent))

from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import Qt
from ui.main_window import MainWindow


def excepthook(exc_type, exc_value, exc_traceback):
    """Handle unhandled exceptions to prevent app crashes."""
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    
    error_msg = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    print(f"Unhandled exception: {error_msg}", file=sys.stderr)
    
    # Show error dialog if QApplication exists
    app = QApplication.instance()
    if app is not None:
        QMessageBox.critical(
            None,
            "Application Error",
            f"An unexpected error occurred:\n\n{str(exc_value)}\n\n"
            "The application will continue running. Please report this error if it persists."
        )


def main():
    """Main function to run the application."""
    # Install exception hook to catch unhandled exceptions
    sys.excepthook = excepthook
    
    app = QApplication(sys.argv)
    app.setApplicationName("Document Management Client")
    app.setOrganizationName("DMS Client")
    
    try:
        # Create and show main window
        window = MainWindow()
        window.show()
        
        # Run application
        sys.exit(app.exec_())
    except Exception as e:
        print(f"Fatal error during startup: {e}", file=sys.stderr)
        traceback.print_exc()
        QMessageBox.critical(
            None,
            "Startup Error",
            f"Failed to start the application:\n\n{str(e)}\n\nPlease check the console for details."
        )
        sys.exit(1)


if __name__ == "__main__":
    main()

