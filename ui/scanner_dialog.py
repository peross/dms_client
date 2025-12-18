"""Scanner dialog for scanning documents."""
import os
from pathlib import Path
from datetime import datetime
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox,
    QSpinBox, QGroupBox, QProgressBar, QMessageBox, QFileDialog, QGridLayout
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QPixmap, QImage, QFont
from services.scanner_service import ScannerService, ScanThread
from ui.styles import COLORS


class ScannerDialog(QDialog):
    """Dialog for scanning documents."""
    
    def __init__(self, save_directory=None, parent=None):
        """
        Initialize scanner dialog.
        
        Args:
            save_directory (str): Default directory to save scanned documents
            parent: Parent widget
        """
        super().__init__(parent)
        self.save_directory = save_directory
        self.scanned_image = None
        self.scanner_service = ScannerService()
        self.scan_thread = None
        self.init_ui()
        self.detect_scanners()
    
    def init_ui(self):
        """Initialize the UI components."""
        self.setWindowTitle("Scan Document")
        self.setMinimumWidth(600)
        self.setMinimumHeight(500)
        
        layout = QVBoxLayout()
        layout.setSpacing(16)
        layout.setContentsMargins(24, 24, 24, 24)
        
        # Title
        title_label = QLabel("📄 Scan Document")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setWeight(QFont.Bold)
        title_label.setFont(title_font)
        title_label.setStyleSheet(f"color: {COLORS['text_primary']}; padding-bottom: 8px;")
        layout.addWidget(title_label)
        
        # Scanner selection
        scanner_group = QGroupBox("Scanner")
        scanner_group.setStyleSheet(f"""
            QGroupBox {{
                font-weight: 600;
                border: 1px solid {COLORS['border']};
                border-radius: 6px;
                margin-top: 12px;
                padding-top: 12px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 8px;
            }}
        """)
        scanner_layout = QGridLayout()
        scanner_layout.setSpacing(12)
        
        scanner_label = QLabel("Scanner:")
        self.scanner_combo = QComboBox()
        self.scanner_combo.setMinimumWidth(300)
        self.refresh_button = QPushButton("🔄 Refresh")
        self.refresh_button.setProperty("styleClass", "secondary")
        self.refresh_button.clicked.connect(self.detect_scanners)
        scanner_layout.addWidget(scanner_label, 0, 0)
        scanner_layout.addWidget(self.scanner_combo, 0, 1)
        scanner_layout.addWidget(self.refresh_button, 0, 2)
        
        scanner_group.setLayout(scanner_layout)
        layout.addWidget(scanner_group)
        
        # Scan settings
        settings_group = QGroupBox("Scan Settings")
        settings_group.setStyleSheet(scanner_group.styleSheet())
        settings_layout = QGridLayout()
        settings_layout.setSpacing(12)
        
        # Resolution
        resolution_label = QLabel("Resolution (DPI):")
        self.resolution_spin = QSpinBox()
        self.resolution_spin.setMinimum(72)
        self.resolution_spin.setMaximum(1200)
        self.resolution_spin.setValue(300)
        self.resolution_spin.setSingleStep(50)
        settings_layout.addWidget(resolution_label, 0, 0)
        settings_layout.addWidget(self.resolution_spin, 0, 1)
        
        # Color mode
        mode_label = QLabel("Color Mode:")
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["Color", "Gray", "Lineart"])
        settings_layout.addWidget(mode_label, 1, 0)
        settings_layout.addWidget(self.mode_combo, 1, 1)
        
        # Format
        format_label = QLabel("Save Format:")
        self.format_combo = QComboBox()
        self.format_combo.addItems(["PNG", "JPEG", "PDF"])
        settings_layout.addWidget(format_label, 2, 0)
        settings_layout.addWidget(self.format_combo, 2, 1)
        
        settings_group.setLayout(settings_layout)
        layout.addWidget(settings_group)
        
        # Preview area
        preview_group = QGroupBox("Preview")
        preview_group.setStyleSheet(scanner_group.styleSheet())
        preview_layout = QVBoxLayout()
        
        self.preview_label = QLabel("No preview available")
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.preview_label.setMinimumHeight(200)
        self.preview_label.setStyleSheet(f"""
            QLabel {{
                background-color: {COLORS['surface']};
                border: 1px solid {COLORS['border']};
                border-radius: 6px;
            }}
        """)
        preview_layout.addWidget(self.preview_label)
        
        preview_group.setLayout(preview_layout)
        layout.addWidget(preview_group)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setTextVisible(False)
        layout.addWidget(self.progress_bar)
        
        # Status label
        self.status_label = QLabel("Ready to scan")
        self.status_label.setStyleSheet(f"color: {COLORS['text_secondary']}; padding: 8px;")
        layout.addWidget(self.status_label)
        
        layout.addStretch()
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(12)
        
        self.scan_button = QPushButton("📄 Scan Document")
        self.scan_button.clicked.connect(self.start_scan)
        button_layout.addWidget(self.scan_button)
        
        button_layout.addStretch()
        
        save_button = QPushButton("💾 Save")
        save_button.setEnabled(False)
        save_button.setProperty("styleClass", "secondary")
        save_button.clicked.connect(self.save_scanned_document)
        button_layout.addWidget(save_button)
        self.save_button = save_button
        
        cancel_button = QPushButton("Cancel")
        cancel_button.setProperty("styleClass", "secondary")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
    
    def detect_scanners(self):
        """Detect available scanners."""
        self.status_label.setText("Detecting scanners...")
        self.scanner_combo.clear()
        self.refresh_button.setEnabled(False)
        
        scanners = self.scanner_service.detect_scanners()
        
        if scanners:
            for scanner in scanners:
                display_name = f"{scanner.get('vendor', 'Unknown')} {scanner.get('model', scanner.get('name', 'Unknown'))}"
                self.scanner_combo.addItem(display_name, scanner)
            self.status_label.setText(f"Found {len(scanners)} scanner(s)")
        else:
            self.scanner_combo.addItem("No scanners found")
            self.status_label.setText("No scanners detected. Make sure your scanner is connected and drivers are installed.")
            self.scan_button.setEnabled(False)
        
        self.refresh_button.setEnabled(True)
    
    def start_scan(self):
        """Start scanning document."""
        if self.scanner_combo.count() == 0 or self.scanner_combo.currentText() == "No scanners found":
            QMessageBox.warning(self, "No Scanner", "No scanner selected. Please refresh and select a scanner.")
            return
        
        scanner_index = self.scanner_combo.currentIndex()
        resolution = self.resolution_spin.value()
        mode = self.mode_combo.currentText()
        format_type = self.format_combo.currentText()
        
        # Generate save path - we'll save manually after scan, so don't auto-save here
        # This allows us to preview first and handle save location properly
        save_path = None  # Don't auto-save, let user preview first
        
        # Disable scan button during scan
        self.scan_button.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Indeterminate progress
        self.status_label.setText("Scanning... Please wait")
        
        # Create and start scan thread
        self.scan_thread = ScanThread(
            self.scanner_service,
            scanner_index,
            resolution,
            mode,
            format_type,
            save_path
        )
        self.scan_thread.scan_complete.connect(self.on_scan_complete)
        self.scan_thread.scan_error.connect(self.on_scan_error)
        self.scan_thread.scan_progress.connect(self.on_scan_progress)
        self.scan_thread.finished.connect(self.on_scan_finished)
        self.scan_thread.start()
    
    def on_scan_progress(self, message):
        """Handle scan progress update."""
        self.status_label.setText(message)
    
    def on_scan_complete(self, image):
        """Handle scan completion."""
        from PIL.ImageQt import ImageQt
        
        self.scanned_image = image
        
        # Convert PIL image to QPixmap for preview
        try:
            q_image = ImageQt(image)
            pixmap = QPixmap.fromImage(q_image)
            
            # Scale preview to fit label
            label_size = self.preview_label.size()
            scaled_pixmap = pixmap.scaled(
                label_size.width() - 20,
                label_size.height() - 20,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.preview_label.setPixmap(scaled_pixmap)
            
            # If we have a save directory, auto-save
            if self.save_directory and os.path.exists(self.save_directory):
                self.auto_save_scanned_document()
            else:
                self.status_label.setText("Scan complete! Preview displayed above. Click Save to save the document.")
        except Exception as e:
            self.status_label.setText(f"Scan complete, but preview error: {str(e)}")
        
        self.save_button.setEnabled(True)
    
    def on_scan_error(self, error_message):
        """Handle scan error."""
        QMessageBox.critical(self, "Scan Error", error_message)
        self.status_label.setText("Error during scan")
    
    def on_scan_finished(self):
        """Handle scan thread finished."""
        self.scan_button.setEnabled(True)
        self.progress_bar.setVisible(False)
    
    def auto_save_scanned_document(self):
        """Automatically save the scanned document to the save directory."""
        if not self.scanned_image or not self.save_directory:
            return
        
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            format_type = self.format_combo.currentText()
            extension = format_type.lower()
            if extension == 'jpeg':
                extension = 'jpg'
            
            file_path = os.path.join(self.save_directory, f"scan_{timestamp}.{extension}")
            
            # Handle image mode conversion for different formats
            image = self.scanned_image.copy()
            if format_type.upper() == 'PDF':
                if image.mode != 'RGB':
                    image = image.convert('RGB')
                image.save(file_path, 'PDF')
            elif format_type.upper() == 'JPEG':
                if image.mode != 'RGB':
                    image = image.convert('RGB')
                image.save(file_path, 'JPEG', quality=95)
            else:
                image.save(file_path, 'PNG')
            
            self.status_label.setText(f"Saved to: {Path(file_path).name}")
            # Close dialog after successful auto-save
            self.accept()
        except Exception as e:
            self.status_label.setText(f"Auto-save error: {str(e)}")
            QMessageBox.warning(self, "Save Warning", f"Auto-save failed:\n{str(e)}\n\nPlease use Save button to save manually.")
    
    def save_scanned_document(self):
        """Save the scanned document to a user-selected location."""
        if not self.scanned_image:
            QMessageBox.warning(self, "No Image", "No scanned image to save.")
            return
        
        # Get save path
        default_dir = self.save_directory or str(Path.home())
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        format_type = self.format_combo.currentText()
        extension = format_type.lower()
        if extension == 'jpeg':
            extension = 'jpg'
        
        default_filename = f"scan_{timestamp}.{extension}"
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Scanned Document",
            os.path.join(default_dir, default_filename),
            f"{format_type} Files (*.{extension});;All Files (*)"
        )
        
        if file_path:
            try:
                # Handle image mode conversion
                image = self.scanned_image.copy()
                if format_type.upper() == 'PDF':
                    if image.mode != 'RGB':
                        image = image.convert('RGB')
                    image.save(file_path, 'PDF')
                elif format_type.upper() == 'JPEG':
                    if image.mode != 'RGB':
                        image = image.convert('RGB')
                    image.save(file_path, 'JPEG', quality=95)
                else:
                    image.save(file_path, 'PNG')
                
                QMessageBox.information(self, "Success", f"Document saved to:\n{file_path}")
                self.status_label.setText(f"Saved to: {Path(file_path).name}")
                self.accept()
            except Exception as e:
                QMessageBox.critical(self, "Save Error", f"Error saving file:\n{str(e)}")
    
    def get_scanned_image(self):
        """
        Get the scanned image.
        
        Returns:
            PIL.Image: Scanned image, or None
        """
        return self.scanned_image

