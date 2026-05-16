#!/usr/bin/env python3
"""
Tests for config utility
"""

import unittest
import tempfile
import shutil
from pathlib import Path
from mcpforge.utils.config import ConfigManager


class TestConfigManager(unittest.TestCase):
    """Test cases for ConfigManager."""
    
    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.original_config_dir = ConfigManager.CONFIG_DIR
        ConfigManager.CONFIG_DIR = Path(self.temp_dir) / ".config" / "mcpforge"
        ConfigManager.CONFIG_FILE = ConfigManager.CONFIG_DIR / "config.json"
    
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir)
        ConfigManager.CONFIG_DIR = self.original_config_dir
    
    def test_default_config(self):
        """Test default configuration values."""
        config = ConfigManager()
        self.assertEqual(config.get("version"), "1.0.0")
        self.assertEqual(config.get("default_transport"), "stdio")
    
    def test_set_and_get(self):
        """Test setting and getting configuration values."""
        config = ConfigManager()
        config.set("test_key", "test_value")
        self.assertEqual(config.get("test_key"), "test_value")
    
    def test_save_and_load(self):
        """Test saving and loading configuration."""
        config = ConfigManager()
        config.set("test_key", "test_value")
        
        # Create new instance to test loading
        config2 = ConfigManager()
        self.assertEqual(config2.get("test_key"), "test_value")


if __name__ == "__main__":
    unittest.main()
