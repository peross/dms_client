"""Folder management service for creating default folders."""
import os
from pathlib import Path


class FolderManager:
    """Manages default folder creation and validation."""
    
    DEFAULT_FOLDERS = [
        "General",
        "My Folders",
        "Shared With Me"
    ]
    
    @staticmethod
    def validate_location(location_path):
        """
        Validate that a location can be used for tracking.
        
        Args:
            location_path (str): Path to validate
            
        Returns:
            tuple: (is_valid, error_message)
                  is_valid: True if location is valid, False otherwise
                  error_message: Error message if invalid, None if valid
        """
        path = Path(location_path)
        
        if not path.exists():
            return False, "Location does not exist"
        
        if not path.is_dir():
            return False, "Location is not a directory"
        
        # Check if location is writable
        if not os.access(path, os.W_OK):
            return False, "Location is not writable"
        
        return True, None
    
    @staticmethod
    def create_default_folders(base_path):
        """
        Create default folders in the specified location.
        
        Args:
            base_path (str): Base path where folders should be created
            
        Returns:
            list: List of created folder paths (strings)
        """
        base = Path(base_path)
        created_folders = []
        
        for folder_name in FolderManager.DEFAULT_FOLDERS:
            folder_path = base / folder_name
            try:
                folder_path.mkdir(exist_ok=True)
                created_folders.append(str(folder_path))
            except (OSError, PermissionError) as e:
                # Log error but continue with other folders
                print(f"Warning: Could not create folder {folder_name}: {e}")
        
        return created_folders
    
    @staticmethod
    def get_default_folder_paths(base_path):
        """
        Get paths to all default folders.
        
        Args:
            base_path (str): Base path
            
        Returns:
            list: List of folder paths
        """
        base = Path(base_path)
        return [str(base / folder_name) for folder_name in FolderManager.DEFAULT_FOLDERS]
    
    @staticmethod
    def folders_exist(base_path):
        """
        Check if default folders already exist.
        
        Args:
            base_path (str): Base path to check
            
        Returns:
            bool: True if all default folders exist, False otherwise
        """
        base = Path(base_path)
        return all((base / folder_name).exists() for folder_name in FolderManager.DEFAULT_FOLDERS)

