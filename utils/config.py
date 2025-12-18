"""Configuration management for DMS Client."""
import json
import os
from pathlib import Path


class Config:
    """Manages application configuration."""
    
    CONFIG_DIR_NAME = ".dms_client"
    CONFIG_FILE_NAME = "config.json"
    
    def __init__(self):
        """Initialize configuration manager."""
        self.config_dir = Path.home() / self.CONFIG_DIR_NAME
        self.config_file = self.config_dir / self.CONFIG_FILE_NAME
        self._ensure_config_dir()
    
    def _ensure_config_dir(self):
        """Create config directory if it doesn't exist."""
        self.config_dir.mkdir(exist_ok=True)
    
    def get_tracked_location(self):
        """
        Get the currently tracked location.
        
        Returns:
            str: Path to tracked location, or None if not set
        """
        if not self.config_file.exists():
            return None
        
        try:
            with open(self.config_file, 'r') as f:
                config = json.load(f)
                return config.get('tracked_location')
        except (json.JSONDecodeError, IOError):
            return None
    
    def set_tracked_location(self, path):
        """
        Set the tracked location.
        
        Args:
            path (str): Path to the location to track
        """
        config = {}
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
            except (json.JSONDecodeError, IOError):
                config = {}
        
        config['tracked_location'] = str(path)
        
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)
    
    def has_tracked_location(self):
        """
        Check if a tracked location is configured.
        
        Returns:
            bool: True if location is configured, False otherwise
        """
        return self.get_tracked_location() is not None

