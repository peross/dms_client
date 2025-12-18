"""Main application window."""
from PyQt5.QtWidgets import (
    QMainWindow, QMenuBar, QMenu, QAction, QStatusBar, QMessageBox, QToolBar
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from ui.file_browser import FileBrowser
from ui.location_dialog import LocationDialog
from ui.scanner_dialog import ScannerDialog
from ui.styles import get_modern_stylesheet
from services.file_watcher import FileWatcher
from utils.config import Config


class MainWindow(QMainWindow):
    """Main window for the DMS Client application."""
    
    def __init__(self, parent=None):
        """
        Initialize main window.
        
        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self.config = Config()
        self.file_watcher = FileWatcher()
        self.file_browser = None
        self.init_ui()
        self.load_tracked_location()
        self.connect_file_watcher_signals()
    
    def init_ui(self):
        """Initialize the UI components."""
        self.setWindowTitle("Document Management Client")
        self.setGeometry(100, 100, 1200, 800)
        
        # Apply modern stylesheet
        self.setStyleSheet(get_modern_stylesheet())
        
        # Create menu bar
        self.create_menu_bar()
        
        # Create toolbar
        self.create_toolbar()
        
        # Create file browser
        self.file_browser = FileBrowser()
        self.setCentralWidget(self.file_browser)
        
        # Create status bar
        self.create_status_bar()
    
    def create_menu_bar(self):
        """Create the menu bar."""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("&File")
        
        select_location_action = QAction("&Select Location...", self)
        select_location_action.setShortcut("Ctrl+O")
        select_location_action.setStatusTip("Choose a directory to track")
        select_location_action.triggered.connect(self.select_location)
        file_menu.addAction(select_location_action)
        
        scan_document_action = QAction("&Scan Document...", self)
        scan_document_action.setShortcut("Ctrl+Shift+S")
        scan_document_action.setStatusTip("Scan a document using connected scanner")
        scan_document_action.triggered.connect(self.scan_document)
        file_menu.addAction(scan_document_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("E&xit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.setStatusTip("Exit the application")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # View menu
        view_menu = menubar.addMenu("&View")
        
        self.list_view_action = QAction("&List View", self)
        self.list_view_action.setCheckable(True)
        self.list_view_action.setChecked(True)
        self.list_view_action.setShortcut("Ctrl+1")
        self.list_view_action.triggered.connect(lambda: self.set_view_mode(FileBrowser.VIEW_LIST))
        view_menu.addAction(self.list_view_action)
        
        self.tree_view_action = QAction("&Tree View", self)
        self.tree_view_action.setCheckable(True)
        self.tree_view_action.setShortcut("Ctrl+2")
        self.tree_view_action.triggered.connect(lambda: self.set_view_mode(FileBrowser.VIEW_TREE))
        view_menu.addAction(self.tree_view_action)
        
        self.grid_view_action = QAction("&Grid View", self)
        self.grid_view_action.setCheckable(True)
        self.grid_view_action.setShortcut("Ctrl+3")
        self.grid_view_action.triggered.connect(lambda: self.set_view_mode(FileBrowser.VIEW_GRID))
        view_menu.addAction(self.grid_view_action)
        
        # Help menu
        help_menu = menubar.addMenu("&Help")
        
        about_action = QAction("&About", self)
        about_action.setStatusTip("About Document Management Client")
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def create_toolbar(self):
        """Create the toolbar."""
        toolbar = QToolBar("Main Toolbar")
        toolbar.setMovable(False)
        self.addToolBar(toolbar)
        
        # Select location action
        select_location_action = QAction("📁 Select Location", self)
        select_location_action.setToolTip("Select Location (Ctrl+O)")
        select_location_action.setStatusTip("Choose a directory to track")
        select_location_action.triggered.connect(self.select_location)
        toolbar.addAction(select_location_action)
        
        toolbar.addSeparator()
        
        # Scan document action
        scan_action = QAction("📄 Scan Document", self)
        scan_action.setToolTip("Scan Document (Ctrl+Shift+S)")
        scan_action.setStatusTip("Scan a document using connected scanner")
        scan_action.setShortcut("Ctrl+Shift+S")
        scan_action.triggered.connect(self.scan_document)
        toolbar.addAction(scan_action)
        
        toolbar.addSeparator()
        
        # View mode actions
        list_view_action = QAction("☰ List", self)
        list_view_action.setToolTip("List View (Ctrl+1)")
        list_view_action.setCheckable(True)
        list_view_action.setChecked(True)
        list_view_action.triggered.connect(lambda: self.set_view_mode(FileBrowser.VIEW_LIST))
        toolbar.addAction(list_view_action)
        
        tree_view_action = QAction("🌳 Tree", self)
        tree_view_action.setToolTip("Tree View (Ctrl+2)")
        tree_view_action.setCheckable(True)
        tree_view_action.triggered.connect(lambda: self.set_view_mode(FileBrowser.VIEW_TREE))
        toolbar.addAction(tree_view_action)
        
        grid_view_action = QAction("⊞ Grid", self)
        grid_view_action.setToolTip("Grid View (Ctrl+3)")
        grid_view_action.setCheckable(True)
        grid_view_action.triggered.connect(lambda: self.set_view_mode(FileBrowser.VIEW_GRID))
        toolbar.addAction(grid_view_action)
        
        # Store references for updating check state
        self.toolbar_list_action = list_view_action
        self.toolbar_tree_action = tree_view_action
        self.toolbar_grid_action = grid_view_action
    
    def create_status_bar(self):
        """Create the status bar."""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.update_status_bar("Ready")
    
    def update_status_bar(self, message):
        """
        Update status bar message.
        
        Args:
            message (str): Message to display
        """
        self.status_bar.showMessage(message)
    
    def set_view_mode(self, mode):
        """
        Set the file browser view mode.
        
        Args:
            mode (int): View mode constant
        """
        if self.file_browser:
            self.file_browser.set_current_view(mode)
            # Update check states
            self.list_view_action.setChecked(mode == FileBrowser.VIEW_LIST)
            self.tree_view_action.setChecked(mode == FileBrowser.VIEW_TREE)
            self.grid_view_action.setChecked(mode == FileBrowser.VIEW_GRID)
            if hasattr(self, 'toolbar_list_action'):
                self.toolbar_list_action.setChecked(mode == FileBrowser.VIEW_LIST)
                self.toolbar_tree_action.setChecked(mode == FileBrowser.VIEW_TREE)
                self.toolbar_grid_action.setChecked(mode == FileBrowser.VIEW_GRID)
    
    def select_location(self):
        """Show location selection dialog."""
        current_location = self.config.get_tracked_location()
        dialog = LocationDialog(current_location, self)
        
        if dialog.exec_() == LocationDialog.Accepted:
            new_location = dialog.get_selected_location()
            if new_location:
                self.config.set_tracked_location(new_location)
                self.load_tracked_location()
                QMessageBox.information(
                    self,
                    "Location Set",
                    f"Now tracking location:\n{new_location}"
                )
    
    def load_tracked_location(self):
        """Load the tracked location from config and start monitoring."""
        tracked_location = self.config.get_tracked_location()
        
        if tracked_location:
            from pathlib import Path
            if Path(tracked_location).exists():
                # Set location in file browser
                self.file_browser.set_tracked_location(tracked_location)
                
                # Start file watcher
                if self.file_watcher.start_watching(tracked_location):
                    self.update_status_bar(f"Tracking: {tracked_location}")
                else:
                    self.update_status_bar(f"Error starting file watcher for: {tracked_location}")
            else:
                QMessageBox.warning(
                    self,
                    "Location Not Found",
                    f"The tracked location no longer exists:\n{tracked_location}\n\nPlease select a new location."
                )
                self.config.set_tracked_location(None)
                self.update_status_bar("No location tracked")
        else:
            # No location configured, ask user to select one
            self.update_status_bar("No location tracked. Please select a location from File menu.")
            if self.file_browser:
                self.file_browser.set_tracked_location(None)
    
    def connect_file_watcher_signals(self):
        """Connect file watcher signals to update UI."""
        if self.file_watcher:
            self.file_watcher.file_created.connect(self.on_file_changed)
            self.file_watcher.file_deleted.connect(self.on_file_changed)
            self.file_watcher.file_modified.connect(self.on_file_changed)
            self.file_watcher.file_moved.connect(self.on_file_moved)
    
    def on_file_changed(self, file_path):
        """
        Handle file change events.
        
        Args:
            file_path (str): Path to the changed file
        """
        # Refresh file browser to show changes
        if self.file_browser:
            self.file_browser.refresh()
    
    def on_file_moved(self, src_path, dest_path):
        """
        Handle file moved events.
        
        Args:
            src_path (str): Source path
            dest_path (str): Destination path
        """
                # Refresh file browser to show changes
        if self.file_browser:
            self.file_browser.refresh()
    
    def scan_document(self):
        """Show scanner dialog to scan a document."""
        # Get the current directory or tracked location for saving
        save_directory = None
        if self.file_browser and self.file_browser.current_path:
            save_directory = self.file_browser.current_path
        elif self.config.get_tracked_location():
            save_directory = self.config.get_tracked_location()
        
        dialog = ScannerDialog(save_directory, self)
        
        if dialog.exec_() == ScannerDialog.Accepted:
            # Refresh file browser to show new scanned document
            if self.file_browser:
                self.file_browser.refresh()
            self.update_status_bar("Document scanned successfully")
    
    def show_about(self):
        """Show about dialog."""
        QMessageBox.about(
            self,
            "About Document Management Client",
            "Document Management Client\n\n"
            "A cross-platform application for managing documents\n"
            "with real-time file tracking.\n\n"
            "Version 1.0"
        )
    
    def closeEvent(self, event):
        """Handle window close event."""
        # Stop file watcher
        if self.file_watcher:
            self.file_watcher.stop_watching()
        event.accept()

