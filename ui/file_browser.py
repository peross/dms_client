"""File browser widget with multiple view modes."""
import os
from pathlib import Path
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QListView, QTreeView,
    QFileSystemModel, QLineEdit, QLabel, QPushButton, QStackedWidget, QFrame
)
from PyQt5.QtCore import Qt, QDir, QModelIndex, pyqtSignal, QSize
from PyQt5.QtGui import QFont
from services.folder_manager import FolderManager
from ui.styles import COLORS


class FileBrowser(QWidget):
    """File browser widget with list, tree, and grid view modes."""
    
    # Signal emitted when file selection changes
    file_selected = pyqtSignal(str)  # File path
    
    VIEW_LIST = 0
    VIEW_TREE = 1
    VIEW_GRID = 2
    
    def __init__(self, parent=None):
        """
        Initialize file browser.
        
        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self.tracked_location = None
        self.current_path = None  # Current directory being viewed
        self.current_view = self.VIEW_LIST
        self.model = None
        self.list_view = None
        self.tree_view = None
        self.grid_view = None
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI components."""
        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(16, 16, 16, 16)
        
        # Header section with title and search
        header_frame = QFrame()
        header_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['surface']};
                border-radius: 8px;
                padding: 12px;
            }}
        """)
        header_layout = QVBoxLayout()
        header_layout.setSpacing(8)
        header_frame.setLayout(header_layout)
        
        # Title
        title_label = QLabel("📄 Documents")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setWeight(QFont.Bold)
        title_label.setFont(title_font)
        title_label.setStyleSheet(f"color: {COLORS['text_primary']}; padding-bottom: 4px;")
        header_layout.addWidget(title_label)
        
        # Navigation and search bar
        nav_search_layout = QHBoxLayout()
        nav_search_layout.setSpacing(8)
        
        # Navigation buttons
        nav_layout = QHBoxLayout()
        nav_layout.setSpacing(4)
        
        self.back_button = QPushButton("◀ Back")
        self.back_button.setProperty("styleClass", "secondary")
        self.back_button.setToolTip("Go to parent directory")
        self.back_button.setMaximumWidth(80)
        self.back_button.clicked.connect(self.navigate_back)
        nav_layout.addWidget(self.back_button)
        
        self.up_button = QPushButton("↑ Up")
        self.up_button.setProperty("styleClass", "secondary")
        self.up_button.setToolTip("Go up one level")
        self.up_button.setMaximumWidth(70)
        self.up_button.clicked.connect(self.navigate_up)
        nav_layout.addWidget(self.up_button)
        
        nav_search_layout.addLayout(nav_layout)
        nav_search_layout.addStretch()
        
        # Search
        search_label = QLabel("🔍")
        search_label.setStyleSheet(f"color: {COLORS['text_secondary']};")
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Search files and folders...")
        self.search_edit.textChanged.connect(self.filter_files)
        self.search_edit.setClearButtonEnabled(True)
        self.search_edit.setMaximumWidth(300)
        nav_search_layout.addWidget(search_label)
        nav_search_layout.addWidget(self.search_edit)
        
        header_layout.addLayout(nav_search_layout)
        
        layout.addWidget(header_frame)
        
        # Stacked widget for different views
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setStyleSheet(f"""
            QStackedWidget {{
                background-color: {COLORS['background']};
                border-radius: 8px;
            }}
        """)
        
        # List view
        self.list_view = QListView()
        self.list_view.setViewMode(QListView.ListMode)
        self.list_view.setSpacing(4)
        self.list_view.doubleClicked.connect(self.on_item_double_clicked)
        self.list_view.setUniformItemSizes(True)
        self.stacked_widget.addWidget(self.list_view)
        
        # Tree view
        self.tree_view = QTreeView()
        self.tree_view.setHeaderHidden(False)
        self.tree_view.setRootIsDecorated(True)
        self.tree_view.setAnimated(True)
        self.tree_view.setAlternatingRowColors(True)
        self.tree_view.doubleClicked.connect(self.on_item_double_clicked)
        self.stacked_widget.addWidget(self.tree_view)
        
        # Grid view (using QListView in icon mode)
        self.grid_view = QListView()
        self.grid_view.setViewMode(QListView.IconMode)
        self.grid_view.setResizeMode(QListView.Adjust)
        self.grid_view.setGridSize(QSize(120, 120))
        self.grid_view.setSpacing(12)
        self.grid_view.doubleClicked.connect(self.on_item_double_clicked)
        self.grid_view.setUniformItemSizes(True)
        self.stacked_widget.addWidget(self.grid_view)
        
        layout.addWidget(self.stacked_widget, 1)  # Stretch factor 1
        
        # Status label
        status_frame = QFrame()
        status_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['surface']};
                border-radius: 6px;
                padding: 8px 12px;
            }}
        """)
        status_layout = QHBoxLayout()
        status_layout.setContentsMargins(0, 0, 0, 0)
        status_frame.setLayout(status_layout)
        
        self.status_label = QLabel("No location selected")
        self.status_label.setStyleSheet(f"color: {COLORS['text_secondary']};")
        status_layout.addWidget(self.status_label)
        status_layout.addStretch()
        
        layout.addWidget(status_frame)
        
        self.setLayout(layout)
        self.set_current_view(self.VIEW_LIST)
        
        # Initialize navigation buttons state
        if hasattr(self, 'up_button'):
            self.up_button.setEnabled(False)
            self.back_button.setEnabled(False)
    
    def set_tracked_location(self, path):
        """
        Set the tracked location and update the browser.
        
        Args:
            path (str): Path to track
        """
        self.tracked_location = path
        if not path or not Path(path).exists():
            self.status_label.setText("Invalid location")
            return
        
        # Create file system model
        self.model = QFileSystemModel()
        self.model.setRootPath(path)
        self.model.setFilter(QDir.AllDirs | QDir.Files | QDir.NoDotAndDotDot)
        
        # Get default folder paths
        default_folders = FolderManager.get_default_folder_paths(path)
        
        # Set model for all views
        self.list_view.setModel(self.model)
        self.tree_view.setModel(self.model)
        self.grid_view.setModel(self.model)
        
        # Set root index to tracked location
        self.current_path = path
        root_index = self.model.index(path)
        self.list_view.setRootIndex(root_index)
        self.tree_view.setRootIndex(root_index)
        self.grid_view.setRootIndex(root_index)
        self._update_navigation_buttons()
        
        # Update status
        file_count = self._count_files(path, default_folders)
        folder_count = len([f for f in default_folders if Path(f).exists()])
        self.status_label.setText(
            f"📂 {Path(path).name}  •  {file_count} files  •  {folder_count} folders"
        )
    
    def _count_files(self, base_path, folder_paths):
        """
        Count files in the default folders.
        
        Args:
            base_path (str): Base tracked path
            folder_paths (list): List of folder paths to count
            
        Returns:
            int: Total file count
        """
        count = 0
        for folder_path in folder_paths:
            folder = Path(folder_path)
            if folder.exists():
                count += sum(1 for _ in folder.rglob('*') if _.is_file())
        return count
    
    def set_current_view(self, view_mode):
        """
        Set the current view mode.
        
        Args:
            view_mode (int): View mode constant (VIEW_LIST, VIEW_TREE, VIEW_GRID)
        """
        self.current_view = view_mode
        self.stacked_widget.setCurrentIndex(view_mode)
    
    def on_item_double_clicked(self, index):
        """
        Handle double-click on file item.
        
        Args:
            index (QModelIndex): Model index of the clicked item
        """
        if self.model:
            file_path = self.model.filePath(index)
            file_path_obj = Path(file_path)
            
            if file_path_obj.is_file():
                # Emit signal for file selection
                self.file_selected.emit(file_path)
                # Open file with system default application
                self._open_file(file_path)
            elif file_path_obj.is_dir():
                # Navigate into directory
                self._navigate_to_directory(file_path)
    
    def _open_file(self, file_path):
        """
        Open a file with the system default application.
        
        Args:
            file_path (str): Path to the file to open
        """
        import subprocess
        import sys
        import platform
        
        try:
            if platform.system() == 'Windows':
                os.startfile(file_path)
            elif platform.system() == 'Darwin':  # macOS
                subprocess.run(['open', file_path])
            else:  # Linux and others
                subprocess.run(['xdg-open', file_path])
        except Exception as e:
            print(f"Error opening file {file_path}: {e}")
    
    def _navigate_to_directory(self, directory_path):
        """
        Navigate to a directory in the file browser.
        
        Args:
            directory_path (str): Path to the directory
        """
        if self.model:
            dir_index = self.model.index(directory_path)
            if dir_index.isValid():
                self.current_path = directory_path
                self.list_view.setRootIndex(dir_index)
                self.tree_view.setRootIndex(dir_index)
                self.grid_view.setRootIndex(dir_index)
                self._update_navigation_buttons()
    
    def navigate_back(self):
        """Navigate to the previous directory."""
        # For now, just navigate up (can be enhanced with history)
        self.navigate_up()
    
    def navigate_up(self):
        """Navigate up one level."""
        if self.current_path and self.tracked_location:
            current = Path(self.current_path).resolve()
            tracked = Path(self.tracked_location).resolve()
            parent = current.parent
            
            # Don't go above the tracked location root
            try:
                parent.relative_to(tracked)
                self._navigate_to_directory(str(parent))
            except ValueError:
                # Parent is not relative to tracked location, don't navigate
                pass
    
    def _update_navigation_buttons(self):
        """Update navigation button states."""
        if self.current_path and self.tracked_location:
            current = Path(self.current_path).resolve()
            tracked = Path(self.tracked_location).resolve()
            
            # Enable up button only if we're not at root
            can_go_up = False
            if str(current) != str(tracked):
                try:
                    current.relative_to(tracked)
                    can_go_up = True
                except ValueError:
                    can_go_up = False
            
            self.up_button.setEnabled(can_go_up)
            self.back_button.setEnabled(can_go_up)
    
    def filter_files(self, text):
        """
        Filter files based on search text.
        
        Args:
            text (str): Search text
        """
        if not self.model:
            return
        
        # QFileSystemModel doesn't have built-in filtering,
        # so we'll use name filters
        if text:
            name_filters = [f"*{text}*"]
        else:
            name_filters = ["*"]
        
        self.model.setNameFilters(name_filters)
        self.model.setNameFilterDisables(False)
    
    def refresh(self):
        """Refresh the file browser view while preserving current directory."""
        if self.tracked_location and self.model:
            # Update the model's root path (this refreshes the model)
            self.model.setRootPath(self.tracked_location)
            
            # Preserve the current path if we're in a subdirectory
            # If current_path is not set or invalid, default to tracked_location
            current_path = self.current_path if self.current_path and Path(self.current_path).exists() else self.tracked_location
            
            # Get the index for the current path
            current_index = self.model.index(current_path)
            if current_index.isValid():
                self.current_path = current_path
                # Set root index to current path (preserves navigation)
                self.list_view.setRootIndex(current_index)
                self.tree_view.setRootIndex(current_index)
                self.grid_view.setRootIndex(current_index)
            else:
                # Fallback to tracked location if current path is invalid
                root_index = self.model.index(self.tracked_location)
                self.current_path = self.tracked_location
                self.list_view.setRootIndex(root_index)
                self.tree_view.setRootIndex(root_index)
                self.grid_view.setRootIndex(root_index)
            
            self._update_navigation_buttons()
            
            # Update file count (always count from root)
            default_folders = FolderManager.get_default_folder_paths(self.tracked_location)
            file_count = self._count_files(self.tracked_location, default_folders)
            folder_count = len([f for f in default_folders if Path(f).exists()])
            self.status_label.setText(
                f"📂 {Path(self.tracked_location).name}  •  {file_count} files  •  {folder_count} folders"
            )

