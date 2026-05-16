#!/usr/bin/env python3
"""
Configuration Manager for MCPForge
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, Optional


class ConfigManager:
    """Manage MCPForge configuration."""
    
    CONFIG_DIR = Path.home() / ".config" / "mcpforge"
    CONFIG_FILE = CONFIG_DIR / "config.json"
    REGISTRY_FILE = CONFIG_DIR / "registry.json"
    
    DEFAULT_CONFIG = {
        "version": "1.0.0",
        "default_transport": "stdio",
        "auto_update_check": True,
        "colors_enabled": True,
        "global_packages_dir": str(Path.home() / ".mcpforge" / "global"),
        "npm_registry": "https://registry.npmjs.org",
        "pypi_registry": "https://pypi.org/pypi",
        "timeout": 30,
        "max_retries": 3,
    }
    
    def __init__(self):
        self._config: Dict[str, Any] = {}
        self._ensure_config_dir()
        self.load()
    
    def _ensure_config_dir(self):
        """Ensure configuration directory exists."""
        self.CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        global_dir = Path(self.DEFAULT_CONFIG["global_packages_dir"])
        global_dir.mkdir(parents=True, exist_ok=True)
    
    def load(self) -> Dict[str, Any]:
        """Load configuration from file."""
        if self.CONFIG_FILE.exists():
            try:
                with open(self.CONFIG_FILE, 'r', encoding='utf-8') as f:
                    loaded = json.load(f)
                    self._config = {**self.DEFAULT_CONFIG, **loaded}
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Could not load config: {e}")
                self._config = self.DEFAULT_CONFIG.copy()
        else:
            self._config = self.DEFAULT_CONFIG.copy()
            self.save()
        
        return self._config
    
    def save(self):
        """Save configuration to file."""
        try:
            with open(self.CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(self._config, f, indent=2, ensure_ascii=False)
        except IOError as e:
            print(f"Warning: Could not save config: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        return self._config.get(key, default)
    
    def set(self, key: str, value: Any):
        """Set configuration value."""
        self._config[key] = value
        self.save()
    
    def get_all(self) -> Dict[str, Any]:
        """Get all configuration values."""
        return self._config.copy()
    
    def reset(self):
        """Reset configuration to defaults."""
        self._config = self.DEFAULT_CONFIG.copy()
        self.save()
    
    @property
    def global_packages_dir(self) -> Path:
        """Get global packages directory."""
        return Path(self.get("global_packages_dir"))
    
    @property
    def local_packages_dir(self) -> Path:
        """Get local packages directory (current project)."""
        return Path(".mcpforge") / "packages"


# Global config instance
_config: Optional[ConfigManager] = None


def get_config() -> ConfigManager:
    """Get the global configuration manager instance."""
    global _config
    if _config is None:
        _config = ConfigManager()
    return _config
