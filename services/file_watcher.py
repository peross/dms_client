"""File watcher service using watchdog for real-time file monitoring."""
from pathlib import Path
from PyQt5.QtCore import QObject, pyqtSignal
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileSystemEvent


class FileWatcherEventHandler(FileSystemEventHandler):
    """Event handler for file system events."""
    
    def __init__(self, watcher):
        """
        Initialize event handler.
        
        Args:
            watcher: FileWatcher instance to forward events to
        """
        super().__init__()
        self.watcher = watcher
    
    def on_created(self, event):
        """Handle file/directory created event."""
        if not event.is_directory:
            self.watcher.file_created.emit(event.src_path)
    
    def on_deleted(self, event):
        """Handle file/directory deleted event."""
        if not event.is_directory:
            self.watcher.file_deleted.emit(event.src_path)
    
    def on_modified(self, event):
        """Handle file/directory modified event."""
        if not event.is_directory:
            self.watcher.file_modified.emit(event.src_path)
    
    def on_moved(self, event):
        """Handle file/directory moved event."""
        if not event.is_directory:
            self.watcher.file_moved.emit(event.src_path, event.dest_path)


class FileWatcher(QObject):
    """File watcher service that monitors file system changes."""
    
    # Signals emitted when file events occur
    file_created = pyqtSignal(str)  # File path
    file_deleted = pyqtSignal(str)  # File path
    file_modified = pyqtSignal(str)  # File path
    file_moved = pyqtSignal(str, str)  # Source path, destination path
    
    def __init__(self, parent=None):
        """
        Initialize file watcher.
        
        Args:
            parent: Parent QObject
        """
        super().__init__(parent)
        self.observer = None
        self.tracked_path = None
        self.is_watching = False
    
    def start_watching(self, path):
        """
        Start watching the specified path.
        
        Args:
            path (str): Path to watch (should be the base tracked location)
        """
        if self.is_watching:
            self.stop_watching()
        
        tracked_path = Path(path)
        if not tracked_path.exists():
            return False
        
        try:
            self.observer = Observer()
            event_handler = FileWatcherEventHandler(self)
            self.observer.schedule(event_handler, str(tracked_path), recursive=True)
            self.observer.start()
            self.tracked_path = str(tracked_path)
            self.is_watching = True
            return True
        except Exception as e:
            print(f"Error starting file watcher: {e}")
            return False
    
    def stop_watching(self):
        """Stop watching file changes."""
        if self.observer and self.is_watching:
            try:
                self.observer.stop()
                self.observer.join(timeout=1.0)
            except Exception as e:
                print(f"Error stopping file watcher: {e}")
            finally:
                self.observer = None
                self.is_watching = False
                self.tracked_path = None
    
    def __del__(self):
        """Cleanup on deletion."""
        self.stop_watching()

