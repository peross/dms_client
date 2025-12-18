"""Location selection dialog for choosing tracked location."""
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFileDialog, 
    QMessageBox, QFrame
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from services.folder_manager import FolderManager
from ui.styles import COLORS


class LocationDialog(QDialog):
    """Dialog for selecting the location to track."""
    
    def __init__(self, current_location=None, parent=None):
        """
        Initialize location dialog.
        
        Args:
            current_location (str): Currently tracked location, if any
            parent: Parent widget
        """
        super().__init__(parent)
        self.selected_location = None
        self.current_location = current_location
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI components."""
        self.setWindowTitle("Select Location to Track")
        self.setMinimumWidth(600)
        self.setMinimumHeight(400)
        
        layout = QVBoxLayout()
        layout.setSpacing(16)
        layout.setContentsMargins(24, 24, 24, 24)
        
        # Title
        title_label = QLabel("📁 Select Document Location")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setWeight(QFont.Bold)
        title_label.setFont(title_font)
        title_label.setStyleSheet(f"color: {COLORS['text_primary']}; padding-bottom: 8px;")
        layout.addWidget(title_label)
        
        # Label explaining what to do
        info_label = QLabel(
            "Choose a directory to track for document management.\n"
            "The following default folders will be created:\n\n"
            "  📂 General\n"
            "  📂 My Folders\n"
            "  📂 Shared With Me"
        )
        info_label.setWordWrap(True)
        info_label.setStyleSheet(f"color: {COLORS['text_secondary']}; padding: 12px; background-color: {COLORS['surface']}; border-radius: 6px;")
        layout.addWidget(info_label)
        
        # Current location display
        if self.current_location:
            current_frame = QFrame()
            current_frame.setStyleSheet(f"""
                QFrame {{
                    background-color: {COLORS['surface']};
                    border: 1px solid {COLORS['border']};
                    border-radius: 6px;
                    padding: 12px;
                }}
            """)
            current_layout = QVBoxLayout()
            current_layout.setContentsMargins(0, 0, 0, 0)
            current_label_title = QLabel("Current Location:")
            current_label_title.setStyleSheet(f"color: {COLORS['text_secondary']}; font-weight: 600;")
            current_label = QLabel(self.current_location)
            current_label.setWordWrap(True)
            current_label.setStyleSheet(f"color: {COLORS['text_primary']};")
            current_layout.addWidget(current_label_title)
            current_layout.addWidget(current_label)
            current_frame.setLayout(current_layout)
            layout.addWidget(current_frame)
        
        # Selected location display
        location_frame = QFrame()
        location_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['surface']};
                border: 2px solid {COLORS['border']};
                border-radius: 6px;
                padding: 16px;
                min-height: 80px;
            }}
        """)
        location_layout = QVBoxLayout()
        location_layout.setContentsMargins(0, 0, 0, 0)
        location_title = QLabel("Selected Location:")
        location_title.setStyleSheet(f"color: {COLORS['text_secondary']}; font-weight: 600; padding-bottom: 4px;")
        self.location_label = QLabel("No location selected")
        self.location_label.setWordWrap(True)
        self.location_label.setStyleSheet(f"color: {COLORS['text_primary']};")
        location_layout.addWidget(location_title)
        location_layout.addWidget(self.location_label)
        location_frame.setLayout(location_layout)
        layout.addWidget(location_frame)
        
        # Select button
        self.select_button = QPushButton("📂 Browse for Location...")
        self.select_button.clicked.connect(self.select_location)
        layout.addWidget(self.select_button)
        
        layout.addStretch()
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(12)
        button_layout.addStretch()
        
        cancel_button = QPushButton("Cancel")
        cancel_button.setProperty("styleClass", "secondary")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)
        
        self.ok_button = QPushButton("Continue")
        self.ok_button.setEnabled(False)
        self.ok_button.clicked.connect(self.accept_location)
        button_layout.addWidget(self.ok_button)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
    
    def select_location(self):
        """Open file dialog to select location."""
        start_dir = self.current_location if self.current_location else None
        directory = QFileDialog.getExistingDirectory(
            self,
            "Select Directory to Track",
            start_dir or "",
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
        )
        
        if directory:
            # Validate location
            is_valid, error_message = FolderManager.validate_location(directory)
            
            if is_valid:
                self.selected_location = directory
                self.location_label.setText(directory)
                self.location_label.setStyleSheet(f"color: {COLORS['primary']}; font-weight: 500;")
                self.ok_button.setEnabled(True)
            else:
                QMessageBox.warning(
                    self,
                    "Invalid Location",
                    f"Cannot use this location:\n{error_message}"
                )
                self.selected_location = None
                self.location_label.setText("No location selected")
                self.location_label.setStyleSheet(f"color: {COLORS['text_primary']};")
                self.ok_button.setEnabled(False)
    
    def accept_location(self):
        """Accept the selected location."""
        if self.selected_location:
            # Create default folders
            try:
                FolderManager.create_default_folders(self.selected_location)
                self.accept()
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Error",
                    f"Failed to create default folders:\n{str(e)}"
                )
    
    def get_selected_location(self):
        """
        Get the selected location.
        
        Returns:
            str: Selected location path, or None if cancelled
        """
        return self.selected_location

