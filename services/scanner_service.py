"""Scanner service for detecting and using scanners."""
import platform
import subprocess
import tempfile
import os
from pathlib import Path
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
            list: List of scanner device names (empty list if none found or error)
        """
        self.available_scanners = []
        try:
            # Try to import pyinsane2
            import pyinsane2
            
            # Initialize pyinsane2
            try:
                pyinsane2.init()
            except Exception as init_error:
                # If already initialized, that's OK
                if "already initialized" not in str(init_error).lower():
                    print(f"Warning during pyinsane2.init(): {init_error}")
                # Continue anyway - might work
            
            # Try to get devices
            devices = None
            try:
                devices = pyinsane2.get_devices()
            except Exception as get_devices_error:
                print(f"Error getting devices: {get_devices_error}")
                # Try forcing a refresh
                try:
                    devices = pyinsane2.get_devices(force_reload=True)
                except Exception as refresh_error:
                    print(f"Error refreshing devices: {refresh_error}")
                    # Return empty list - no scanners found
                    return []
            
            if not devices:
                print("No scanners found by pyinsane2")
                # This is not an error - just no scanners available
                return []
            
            if devices:
                for device in devices:
                    try:
                        scanner_info = {
                            'name': device.name,
                            'vendor': getattr(device, 'vendor', 'Unknown'),
                            'model': getattr(device, 'model', 'Unknown'),
                            'device': device
                        }
                        # Try to get additional info
                        try:
                            scanner_info['vendor'] = device.vendor if hasattr(device, 'vendor') else 'Unknown'
                            scanner_info['model'] = device.model if hasattr(device, 'model') else 'Unknown'
                        except:
                            pass
                        
                        self.available_scanners.append(scanner_info)
                        print(f"Found scanner: {scanner_info['vendor']} {scanner_info['model']} ({device.name})")
                    except Exception as device_error:
                        print(f"Error processing device {device}: {device_error}")
                        # Still add it with minimal info
                        self.available_scanners.append({
                            'name': str(device),
                            'vendor': 'Unknown',
                            'model': 'Unknown',
                            'device': device
                        })
            # Note: We're not calling pyinsane2.exit() here because:
            # 1. It might be needed immediately after for scanning
            # 2. pyinsane2 handles cleanup internally
            # 3. Each scan_document() call will handle its own init/exit
            
            return self.available_scanners
        except ImportError:
            # pyinsane2 not installed - this is OK, just return empty list
            print("pyinsane2 not installed. Scanner support unavailable.")
            return []
        except Exception as e:
            # Log the error but don't crash - just return empty list
            error_msg = f"Error detecting scanners: {str(e)}"
            print(f"Scanner detection error (non-fatal): {error_msg}")
            import traceback
            traceback.print_exc()
            # Don't emit error signal - just return empty list
            # The UI will handle showing "No scanners found"
            return []
    
    def _reset_scanner_state(self):
        """Reset scanner state by reinitializing pyinsane2."""
        try:
            import pyinsane2
            try:
                pyinsane2.exit()
            except:
                pass
            import time
            time.sleep(0.3)  # Brief pause to allow scanner to reset
            pyinsane2.init()
            return True
        except Exception as e:
            print(f"Error resetting scanner state: {e}")
            return False
    
    def _scan_with_scanimage(self, scanner, resolution, mode, format_type, device_name=None):
        """
        Fallback method using scanimage command-line tool.
        
        Args:
            scanner: Scanner device object
            resolution: DPI resolution
            mode: Color mode
            format_type: Image format
            
        Returns:
            PIL.Image: Scanned image, or None if failed
        """
        try:
            # Get scanner device name
            if device_name is None:
                if hasattr(scanner, 'name'):
                    device_name = scanner.name
                elif isinstance(scanner, str):
                    device_name = scanner
                else:
                    raise Exception("Cannot determine scanner device name")
            
            # Try to get valid mode - query scanimage directly for mode options
            # This avoids needing to access scanner.options which might be locked
            use_mode_option = False
            scan_mode = None
            
            # Query scanimage for mode constraint
            try:
                query_cmd = ['scanimage', '--device-name', device_name, '--mode', 'help']
                result = subprocess.run(query_cmd, capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    # Parse output to get mode options
                    # Format is usually: mode1|mode2|mode3 [default]
                    output = result.stdout.strip()
                    # Extract mode options (everything before the bracket or newline)
                    if '|' in output:
                        mode_part = output.split('[')[0].strip() if '[' in output else output.split('\n')[0].strip()
                        available_modes = [m.strip() for m in mode_part.split('|')]
                        print(f"Available scanner modes from scanimage: {available_modes}")
                        
                        # Map our mode to available modes
                        mode_lower = mode.lower()
                        if mode_lower == 'color':
                            for m in available_modes:
                                m_str = m.lower()
                                if 'color' in m_str or '24bit' in m_str:
                                    scan_mode = m
                                    use_mode_option = True
                                    print(f"Using mode: {scan_mode}")
                                    break
                        elif mode_lower == 'gray':
                            for m in available_modes:
                                m_str = m.lower()
                                if 'gray' in m_str and 'error' not in m_str:
                                    scan_mode = m
                                    use_mode_option = True
                                    print(f"Using mode: {scan_mode}")
                                    break
                        elif mode_lower == 'lineart':
                            for m in available_modes:
                                m_str = m.lower()
                                if 'black' in m_str or 'white' in m_str:
                                    scan_mode = m
                                    use_mode_option = True
                                    print(f"Using mode: {scan_mode}")
                                    break
            except Exception as mode_error:
                print(f"Could not query scanner modes (will use scanner default): {mode_error}")
                # If we can't get modes, scanimage will use default - that's fine
                pass
            
            # Create temp file for output
            with tempfile.NamedTemporaryFile(suffix='.pnm', delete=False) as tmp_file:
                tmp_path = tmp_file.name
            
            try:
                # Build scanimage command
                cmd = [
                    'scanimage',
                    '--device-name', device_name,
                    '--resolution', str(resolution),
                    '--format', 'pnm'  # Use PNM format (scanimage standard)
                ]
                
                # Only add mode option if we found a valid one
                # Use exact mode string from scanner (may contain spaces/special chars)
                if use_mode_option and scan_mode:
                    # scanimage accepts the mode string as-is, even with spaces/brackets
                    cmd.extend(['--mode', scan_mode])
                
                self.scan_progress.emit("Scanning with scanimage...")
                print(f"Running scanimage command: {' '.join(cmd)}")
                
                # Run scanimage and save to temp file
                # scanimage outputs image data to stdout
                with open(tmp_path, 'wb') as out_file:
                    result = subprocess.run(
                        cmd,
                        stdout=out_file,
                        stderr=subprocess.PIPE,
                        timeout=60  # 60 second timeout
                    )
                
                # Check if we got actual image data
                file_size = os.path.getsize(tmp_path) if os.path.exists(tmp_path) else 0
                error_output = result.stderr.decode('utf-8', errors='ignore')
                
                # scanimage may return 0 even if it fails, or non-zero but still produce output
                # Check for actual image data first
                if file_size > 100:  # PNM files should be at least 100 bytes
                    try:
                        # Try to read the image file
                        image = Image.open(tmp_path)
                        print(f"scanimage produced image: {type(image)}, size: {image.size}")
                        # Success - we have an image despite any error messages
                    except Exception as img_open_error:
                        print(f"Error opening scanimage output: {img_open_error}")
                        # If we can't open it, check the error
                        if result.returncode != 0 or error_output:
                            raise Exception(f"scanimage produced invalid output: {error_output}")
                        raise
                else:
                    # No output file or file is too small (invalid)
                    if result.returncode != 0 or error_output:
                        # Filter out warning messages - check for actual errors
                        error_lines = [line for line in error_output.split('\n') 
                                     if line and 'rounded value' not in line.lower() 
                                     and 'warning' not in line.lower()]
                        if error_lines:
                            error_msg = '\n'.join(error_lines)
                            print(f"scanimage failed: {error_msg}")
                            raise Exception(f"scanimage error: {error_msg}")
                    raise Exception("scanimage produced no output - document may not be in scanner")
                
                # Convert format if needed
                if format_type.upper() == 'JPEG':
                    if image.mode != 'RGB':
                        image = image.convert('RGB')
                elif format_type.upper() == 'PDF':
                    if image.mode != 'RGB':
                        image = image.convert('RGB')
                
                return image
                
            finally:
                # Clean up temp file
                try:
                    if os.path.exists(tmp_path):
                        os.unlink(tmp_path)
                except:
                    pass
                    
        except FileNotFoundError:
            raise Exception("scanimage command not found. Install with: sudo apt install sane-utils")
        except subprocess.TimeoutExpired:
            raise Exception("scanimage timed out. Make sure scanner is ready and document is in place.")
        except Exception as e:
            raise Exception(f"scanimage error: {str(e)}")
    
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
            from pyinsane2.sane.rawapi import SaneException, SaneStatus
            
            # Use scanimage directly for scanning (more reliable than pyinsane2 for some scanners)
            use_scanimage_direct = True
            
            # Get device name - prefer from stored scanner list to avoid pyinsane2 conflicts
            device_name = None
            if self.available_scanners and scanner_index < len(self.available_scanners):
                # Use stored device name from detect_scanners()
                device_name = self.available_scanners[scanner_index]['name']
                print(f"Using device name from stored list: {device_name}")
            else:
                # Fallback: get from pyinsane2 (but exit immediately after to unlock scanner)
                try:
                    pyinsane2.init()
                    devices = pyinsane2.get_devices()
                    if devices and scanner_index < len(devices):
                        device_name = devices[scanner_index].name
                    pyinsane2.exit()  # Exit immediately to release scanner
                    import time
                    time.sleep(0.2)  # Brief pause to ensure scanner is released
                except Exception as e:
                    print(f"Error getting device name from pyinsane2: {e}")
                    self.scan_error.emit(f"Could not get scanner device name: {e}")
                    return None
            
            if not device_name:
                self.scan_error.emit(f"Scanner index {scanner_index} not found")
                return None
            
            if use_scanimage_direct:
                # Use scanimage directly instead of pyinsane2
                # This avoids pyinsane2's image retrieval issues
                self.scan_progress.emit("Scanning with scanimage...")
                try:
                    # Use scanimage method directly with device name
                    # Pass None as scanner object since we're using scanimage directly
                    image = self._scan_with_scanimage(None, resolution, mode, format, device_name=device_name)
                    if image:
                        # Save if path provided
                        if save_path:
                            try:
                                if format.upper() == 'PDF':
                                    if image.mode != 'RGB':
                                        image = image.convert('RGB')
                                    image.save(save_path, 'PDF')
                                elif format.upper() == 'JPEG':
                                    if image.mode != 'RGB':
                                        image = image.convert('RGB')
                                    image.save(save_path, 'JPEG', quality=95)
                                else:
                                    image.save(save_path, 'PNG')
                            except Exception as e:
                                self.scan_error.emit(f"Error saving image: {str(e)}")
                                return None
                        
                        self.scan_complete.emit(image)
                        return image
                    else:
                        raise Exception("scanimage did not produce an image")
                except Exception as scanimage_error:
                    error_msg = f"Error during scanning: {str(scanimage_error)}"
                    print(f"scanimage scan error: {error_msg}")
                    self.scan_error.emit(error_msg)
                    return None
            
            # Fallback pyinsane2 method (should not be reached if use_scanimage_direct is True)
            # Perform scan with pyinsane2
            self.scan_progress.emit("Initializing scan...")
            try:
                scan_session = scanner.scan(multiple=False)
            except SaneException as scan_start_error:
                if "Data is invalid" in str(scan_start_error) or scan_start_error.status == SaneStatus.SANE_STATUS_INVAL:
                    error_msg = (
                        "Scanner is in an invalid state and cannot start scanning.\n\n"
                        "This usually happens when:\n"
                        "1. The scanner was left open from a previous operation\n"
                        "2. Another application is using the scanner\n"
                        "3. The scanner needs to be reset\n\n"
                        "Please try:\n"
                        "1. Close any other applications using the scanner\n"
                        "2. Unplug and replug the USB cable\n"
                        "3. Power cycle the scanner\n"
                        "4. Wait a few seconds and try again"
                    )
                    self.scan_error.emit(error_msg)
                    try:
                        pyinsane2.exit()
                    except:
                        pass
                    return None
                else:
                    raise  # Re-raise if it's a different error
            
            self.scan_progress.emit("Reading scan data...")
            try:
                # Read scan data until EOF
                scan_session.scan.read()
                self.scan_progress.emit("Scanning...")
                
                # Continue reading until EOF
                while True:
                    try:
                        scan_session.scan.read()
                    except EOFError:
                        break
                    except Exception as read_error:
                        # Some scanners might raise different exceptions
                        if "EOF" in str(read_error) or "end of file" in str(read_error).lower():
                            break
                        raise
                        
            except EOFError:
                print("Scan read complete (EOF)")
            except Exception as scan_error:
                error_msg = f"Error reading scan data: {str(scan_error)}"
                print(f"Scan read error: {error_msg}")
                import traceback
                traceback.print_exc()
                self.scan_error.emit(error_msg)
                try:
                    pyinsane2.exit()
                except:
                    pass
                return None
            
            self.scan_progress.emit("Processing scanned image...")
            
            # Get scanned image
            # Try multiple methods to retrieve the image, as pyinsane2 can be tricky
            import time
            time.sleep(0.2)  # Brief pause to let scan finalize
            
            image = None
            error_details = []
            
            try:
                # Method 1: Try get_image() from scan object
                try:
                    if hasattr(scan_session.scan, 'get_image'):
                        image = scan_session.scan.get_image()
                        print(f"SUCCESS: Got image via scan.get_image(): {type(image)}, size: {getattr(image, 'size', 'N/A')}")
                    else:
                        error_details.append("scan.get_image() method not available")
                except Exception as get_img_error:
                    error_msg = f"get_image() failed: {type(get_img_error).__name__}: {get_img_error}"
                    print(error_msg)
                    error_details.append(error_msg)
                
                # Method 2: Try images property from scan_session
                if image is None:
                    try:
                        images_list = scan_session.images
                        print(f"Images property returned: {len(images_list) if images_list else 0} images")
                        if images_list and len(images_list) > 0:
                            image = images_list[0]
                            print(f"SUCCESS: Got image via images property: {type(image)}")
                    except AssertionError as assert_err:
                        error_msg = "AssertionError accessing images property (daemon communication issue)"
                        print(error_msg)
                        error_details.append(error_msg)
                        # This is the known issue - daemon communication breaks
                    except (OSError, Exception) as prop_error:
                        error_msg = f"Error accessing images property: {type(prop_error).__name__}: {prop_error}"
                        print(error_msg)
                        error_details.append(error_msg)
                
                # If both methods failed, try fallback to scanimage command-line tool
                if image is None:
                    print("pyinsane2 image retrieval failed, trying scanimage fallback...")
                    self.scan_progress.emit("Trying alternative scan method...")
                    
                    # Clean up pyinsane2 to free the scanner
                    try:
                        pyinsane2.exit()
                        import time
                        time.sleep(0.5)  # Brief pause to let scanner reset
                    except:
                        pass
                    
                    # Fallback: Use scanimage command-line tool
                    try:
                        image = self._scan_with_scanimage(scanner, resolution, mode, format)
                        if image:
                            print(f"SUCCESS: Got image via scanimage fallback: {type(image)}")
                            # Reinitialize pyinsane2 for future scans
                            try:
                                pyinsane2.init()
                            except:
                                pass
                    except Exception as scanimage_error:
                        print(f"scanimage fallback also failed: {scanimage_error}")
                        # Reinitialize pyinsane2 even if scanimage failed
                        try:
                            pyinsane2.init()
                        except:
                            pass
                        error_msg = (
                            "Unable to retrieve scanned image.\n\n"
                            f"Errors encountered: {'; '.join(error_details)}\n\n"
                            "Both pyinsane2 and scanimage methods failed.\n\n"
                            "Please try:\n"
                            "1. Ensure a document is placed in the scanner\n"
                            "2. Click Refresh and try scanning again\n"
                            "3. Use 'Document Scanner' app as a workaround"
                        )
                        raise ValueError(error_msg)
                
                # If we still don't have an image after all methods, it means no image data
                if image is None:
                    error_msg = (
                        "Scan completed but no image data was received.\n\n"
                        "This can happen if:\n"
                        "1. No document was placed in the scanner\n"
                        "2. The document feeder is empty\n"
                        "3. The scan was cancelled or interrupted\n"
                        "4. Scanner driver communication issue\n\n"
                        "Please ensure:\n"
                        "1. A document is properly placed in/on the scanner\n"
                        "2. The scanner lid is closed (for flatbed scanners)\n"
                        "3. Try scanning again\n"
                        "4. If the problem persists, try restarting the application"
                    )
                    raise ValueError(error_msg)
                    
            except ValueError as ve:
                # Re-raise ValueError with our custom message
                error_msg = str(ve)
                print(f"Image access error: {error_msg}")
                self.scan_error.emit(error_msg)
                try:
                    pyinsane2.exit()
                except:
                    pass
                return None
            except Exception as img_error:
                error_msg = f"Error accessing scanned image: {str(img_error)}"
                print(f"Image access error: {error_msg}")
                import traceback
                traceback.print_exc()
                self.scan_error.emit(error_msg)
                try:
                    pyinsane2.exit()
                except:
                    pass
                return None
            
            if image is not None:
                print(f"Received image type: {type(image)}, mode: {getattr(image, 'mode', 'N/A')}")
                
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
                        error_msg = f"Error converting image: {str(e)}"
                        print(f"Image conversion error: {error_msg}")
                        import traceback
                        traceback.print_exc()
                        self.scan_error.emit(error_msg)
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
                error_msg = "No image data received from scanner. Check scanner connection and try again."
                print(error_msg)
                self.scan_error.emit(error_msg)
                pyinsane2.exit()
                return None
                
        except ImportError:
            error_msg = "pyinsane2 not installed. Install with: pip install pyinsane2"
            self.scan_error.emit(error_msg)
            return None
        except Exception as e:
            error_msg = f"Error during scanning: {str(e)}"
            print(f"Scanner error details: {error_msg}")
            import traceback
            traceback.print_exc()
            self.scan_error.emit(error_msg)
            try:
                pyinsane2.exit()
            except:
                pass
            return None


class DetectScannersThread(QThread):
    """Thread for detecting scanners without blocking UI."""
    
    scanners_detected = pyqtSignal(list)  # List of scanner info dicts
    detection_error = pyqtSignal(str)  # Error message
    detection_progress = pyqtSignal(str)  # Progress message
    
    def __init__(self, scanner_service):
        """
        Initialize scanner detection thread.
        
        Args:
            scanner_service: ScannerService instance
        """
        super().__init__()
        self.scanner_service = scanner_service
    
    def run(self):
        """Run scanner detection in the thread."""
        try:
            self.detection_progress.emit("Detecting scanners...")
            scanners = self.scanner_service.detect_scanners()
            # Always emit scanners_detected signal, even if empty list
            # This allows the UI to handle "no scanners" gracefully
            # Check if thread was requested to stop before emitting
            if not self.isInterruptionRequested():
                self.scanners_detected.emit(scanners if scanners else [])
        except Exception as e:
            # Log error but emit empty list instead of error signal
            # This prevents the app from treating "no scanners" as a fatal error
            print(f"Exception in DetectScannersThread: {e}")
            import traceback
            traceback.print_exc()
            # Emit empty list so UI shows "No scanners found" message
            # Only if thread wasn't interrupted
            if not self.isInterruptionRequested():
                self.scanners_detected.emit([])


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

