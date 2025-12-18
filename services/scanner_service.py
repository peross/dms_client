"""Scanner service for detecting and using scanners."""
import platform
from PyQt5.QtCore import QObject, pyqtSignal, QThread
from PIL import Image


class ScannerService(QObject):
    """Service for detecting and managing scanners."""
    
    # Signals
    scanners_detected = pyqtSignal(list)  # List of scanner names
    scan_complete = pyqtSignal(object)  # PIL Image object
    scan_error = pyqtSignal(str)  # Error message
    scan_progress = pyqtSignal(str)  # Progress message
    
    def __init__(self, parent=None):
        """
        Initialize scanner service.
        
        Args:
            parent: Parent QObject
        """
        super().__init__(parent)
        self.available_scanners = []
        self.current_scanner = None
    
    def detect_scanners(self):
        """
        Detect available scanners on the system.
        
        Returns:
            list: List of scanner device names
        """
        self.available_scanners = []
        try:
            # Try to import pyinsane2
            import pyinsane2
            pyinsane2.init()
            
            devices = pyinsane2.get_devices()
            for device in devices:
                self.available_scanners.append({
                    'name': device.name,
                    'vendor': getattr(device, 'vendor', 'Unknown'),
                    'model': getattr(device, 'model', 'Unknown'),
                    'device': device
                })
            
            pyinsane2.exit()
            return self.available_scanners
        except ImportError:
            self.scan_error.emit("pyinsane2 not installed. Please install it with: pip install pyinsane2")
            return []
        except Exception as e:
            error_msg = f"Error detecting scanners: {str(e)}"
            self.scan_error.emit(error_msg)
            return []
    
    def scan_document(self, scanner_index=0, resolution=300, mode='Color', 
                     format='PNG', save_path=None):
        """
        Scan a document using the specified scanner.
        
        Args:
            scanner_index (int): Index of scanner to use
            resolution (int): DPI resolution (default 300)
            mode (str): Color mode ('Color', 'Gray', 'Lineart')
            format (str): Image format ('PNG', 'JPEG', 'PDF')
            save_path (str): Path to save the scanned document
            
        Returns:
            PIL.Image: Scanned image, or None if error
        """
        try:
            import pyinsane2
            pyinsane2.init()
            
            # Get available devices
            devices = pyinsane2.get_devices()
            if not devices:
                self.scan_error.emit("No scanners found")
                pyinsane2.exit()
                return None
            
            if scanner_index >= len(devices):
                self.scan_error.emit(f"Scanner index {scanner_index} out of range")
                pyinsane2.exit()
                return None
            
            scanner = devices[scanner_index]
            
            self.scan_progress.emit("Configuring scanner...")
            
            # Configure scanner options
            try:
                # Set resolution
                if 'resolution' in scanner.options:
                    scanner.options['resolution'].value = resolution
                
                # Set color mode
                if 'mode' in scanner.options:
                    mode_map = {
                        'Color': 'color',
                        'Gray': 'gray',
                        'Lineart': 'lineart'
                    }
                    sane_mode = mode_map.get(mode, 'color')
                    if sane_mode in scanner.options['mode'].constraint:
                        scanner.options['mode'].value = sane_mode
            except Exception as e:
                self.scan_progress.emit(f"Warning: Could not set all scanner options: {e}")
            
            self.scan_progress.emit("Starting scan...")
            
            # Perform scan
            scan_session = scanner.scan(multiple=False)
            images = []
            
            try:
                while True:
                    scan_session.scan.read()
                    self.scan_progress.emit("Scanning...")
            except EOFError:
                pass
            
            self.scan_progress.emit("Scan complete!")
            
            # Get scanned image
            if scan_session.images:
                image = scan_session.images[0]
                
                # Convert to PIL Image if needed
                # pyinsane2 images are typically PIL Images already, but handle other formats
                if not isinstance(image, Image.Image):
                    try:
                        # Try to convert numpy array to PIL Image
                        import numpy as np
                        if isinstance(image, np.ndarray):
                            image = Image.fromarray(image)
                        else:
                            # Try to convert using Image.open or other methods
                            image = Image.fromarray(image)
                    except Exception as e:
                        self.scan_error.emit(f"Error converting image: {str(e)}")
                        pyinsane2.exit()
                        return None
                
                # Save if path provided
                if save_path:
                    try:
                        if format.upper() == 'PDF':
                            # For PDF, convert to RGB if needed
                            if image.mode != 'RGB':
                                image = image.convert('RGB')
                            image.save(save_path, 'PDF')
                        elif format.upper() == 'JPEG':
                            # JPEG needs RGB mode
                            if image.mode != 'RGB':
                                image = image.convert('RGB')
                            image.save(save_path, 'JPEG', quality=95)
                        else:
                            image.save(save_path, 'PNG')
                    except Exception as e:
                        self.scan_error.emit(f"Error saving image: {str(e)}")
                        pyinsane2.exit()
                        return None
                
                pyinsane2.exit()
                self.scan_complete.emit(image)
                return image
            else:
                self.scan_error.emit("No image data received from scanner")
                pyinsane2.exit()
                return None
                
        except ImportError:
            error_msg = "pyinsane2 not installed. Install with: pip install pyinsane2"
            self.scan_error.emit(error_msg)
            return None
        except Exception as e:
            error_msg = f"Error during scanning: {str(e)}"
            self.scan_error.emit(error_msg)
            try:
                pyinsane2.exit()
            except:
                pass
            return None


class ScanThread(QThread):
    """Thread for performing scans without blocking UI."""
    
    scan_complete = pyqtSignal(object)  # PIL Image
    scan_error = pyqtSignal(str)  # Error message
    scan_progress = pyqtSignal(str)  # Progress message
    
    def __init__(self, scanner_service, scanner_index, resolution, mode, format, save_path):
        """
        Initialize scan thread.
        
        Args:
            scanner_service: ScannerService instance
            scanner_index: Index of scanner to use
            resolution: DPI resolution
            mode: Color mode
            format: Image format
            save_path: Path to save scanned document
        """
        super().__init__()
        self.scanner_service = scanner_service
        self.scanner_index = scanner_index
        self.resolution = resolution
        self.mode = mode
        self.format = format
        self.save_path = save_path
    
    def run(self):
        """Run the scan in the thread."""
        # Connect signals
        self.scanner_service.scan_complete.connect(self.scan_complete.emit)
        self.scanner_service.scan_error.connect(self.scan_error.emit)
        self.scanner_service.scan_progress.connect(self.scan_progress.emit)
        
        # Perform scan
        self.scanner_service.scan_document(
            self.scanner_index,
            self.resolution,
            self.mode,
            self.format,
            self.save_path
        )

