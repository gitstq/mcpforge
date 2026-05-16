#!/usr/bin/env python3
"""
Registry Manager for MCPForge
Manages installed packages and their metadata
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime

from .config import get_config


class RegistryManager:
    """Manage package registry."""
    
    REGISTRY_FILE = "mcpforge.json"
    
    def __init__(self, path: Optional[str] = None):
        self.config = get_config()
        self.global_registry = self.config.global_packages_dir / self.REGISTRY_FILE
        
        if path:
            self.local_registry = Path(path) / self.REGISTRY_FILE
        else:
            self.local_registry = Path(self.REGISTRY_FILE)
    
    def _load_registry(self, registry_path: Path) -> Dict[str, Any]:
        """Load registry from file."""
        if registry_path.exists():
            try:
                with open(registry_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
        return {"packages": {}, "version": "1.0.0"}
    
    def _save_registry(self, registry_path: Path, data: Dict[str, Any]):
        """Save registry to file."""
        registry_path.parent.mkdir(parents=True, exist_ok=True)
        with open(registry_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def install_package(
        self,
        name: str,
        version: str,
        source: str,
        install_path: str,
        metadata: Optional[Dict[str, Any]] = None,
        global_install: bool = False
    ) -> bool:
        """Register an installed package."""
        registry_path = self.global_registry if global_install else self.local_registry
        registry = self._load_registry(registry_path)
        
        registry["packages"][name] = {
            "version": version,
            "source": source,
            "install_path": install_path,
            "installed_at": datetime.now().isoformat(),
            "metadata": metadata or {}
        }
        
        self._save_registry(registry_path, registry)
        return True
    
    def uninstall_package(self, name: str, global_uninstall: bool = False) -> bool:
        """Unregister a package."""
        registry_path = self.global_registry if global_uninstall else self.local_registry
        registry = self._load_registry(registry_path)
        
        if name in registry["packages"]:
            del registry["packages"][name]
            self._save_registry(registry_path, registry)
            return True
        return False
    
    def get_package(self, name: str, global_only: bool = False) -> Optional[Dict[str, Any]]:
        """Get package information."""
        # Check local first
        if not global_only:
            local = self._load_registry(self.local_registry)
            if name in local["packages"]:
                pkg = local["packages"][name].copy()
                pkg["scope"] = "local"
                return pkg
        
        # Check global
        global_reg = self._load_registry(self.global_registry)
        if name in global_reg["packages"]:
            pkg = global_reg["packages"][name].copy()
            pkg["scope"] = "global"
            return pkg
        
        return None
    
    def list_packages(self, global_only: bool = False) -> List[Dict[str, Any]]:
        """List all installed packages."""
        packages = []
        
        if not global_only:
            local = self._load_registry(self.local_registry)
            for name, info in local["packages"].items():
                pkg = info.copy()
                pkg["name"] = name
                pkg["scope"] = "local"
                packages.append(pkg)
        
        global_reg = self._load_registry(self.global_registry)
        for name, info in global_reg["packages"].items():
            pkg = info.copy()
            pkg["name"] = name
            pkg["scope"] = "global"
            packages.append(pkg)
        
        return packages
    
    def is_installed(self, name: str) -> bool:
        """Check if a package is installed."""
        return self.get_package(name) is not None
    
    def get_outdated_packages(self) -> List[Dict[str, Any]]:
        """Get list of outdated packages."""
        outdated = []
        # This would check against remote registries
        # For now, return empty list
        return outdated
    
    def update_package(self, name: str, new_version: str, global_update: bool = False) -> bool:
        """Update package version in registry."""
        registry_path = self.global_registry if global_update else self.local_registry
        registry = self._load_registry(registry_path)
        
        if name in registry["packages"]:
            registry["packages"][name]["version"] = new_version
            registry["packages"][name]["updated_at"] = datetime.now().isoformat()
            self._save_registry(registry_path, registry)
            return True
        return False
