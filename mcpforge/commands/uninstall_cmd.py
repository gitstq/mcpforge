#!/usr/bin/env python3
"""
Uninstall Command - Remove MCP servers and tools
"""

import subprocess
from pathlib import Path
from argparse import Namespace

from mcpforge.utils.formatting import print_success, print_error, print_info, print_warning
from mcpforge.utils.registry import RegistryManager


def execute(args: Namespace) -> int:
    """Execute the uninstall command."""
    package = args.package
    global_uninstall = args.global_uninstall
    
    print_info(f"Uninstalling {package}...")
    
    # Get package info from registry
    registry = RegistryManager()
    pkg_info = registry.get_package(package, global_only=global_uninstall)
    
    if not pkg_info:
        print_warning(f"Package {package} is not installed")
        return 0
    
    source = pkg_info.get("source", "unknown")
    
    if source == "npm":
        return uninstall_npm(package, global_uninstall)
    elif source == "pypi":
        return uninstall_pip(package, global_uninstall)
    elif source == "github":
        return uninstall_github(package, pkg_info.get("install_path", ""), global_uninstall)
    else:
        print_warning(f"Unknown package source: {source}")
        # Still remove from registry
        registry.uninstall_package(package, global_uninstall)
        return 0


def uninstall_npm(package: str, global_uninstall: bool) -> int:
    """Uninstall an NPM package."""
    try:
        cmd = ["npm", "uninstall"]
        if global_uninstall:
            cmd.append("-g")
        cmd.append(package)
        
        print_info(f"Running: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            registry = RegistryManager()
            registry.uninstall_package(package, global_uninstall)
            print_success(f"Successfully uninstalled {package}")
            return 0
        else:
            print_error(f"Failed to uninstall {package}")
            if result.stderr:
                print(result.stderr)
            return 1
    except FileNotFoundError:
        print_error("npm not found.")
        return 1
    except Exception as e:
        print_error(f"Error uninstalling package: {e}")
        return 1


def uninstall_pip(package: str, global_uninstall: bool) -> int:
    """Uninstall a PyPI package."""
    try:
        cmd = ["pip", "uninstall", "-y", package]
        
        print_info(f"Running: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            registry = RegistryManager()
            registry.uninstall_package(package, global_uninstall)
            print_success(f"Successfully uninstalled {package}")
            return 0
        else:
            print_error(f"Failed to uninstall {package}")
            if result.stderr:
                print(result.stderr)
            return 1
    except FileNotFoundError:
        print_error("pip not found.")
        return 1
    except Exception as e:
        print_error(f"Error uninstalling package: {e}")
        return 1


def uninstall_github(package: str, install_path: str, global_uninstall: bool) -> int:
    """Uninstall a GitHub package."""
    try:
        if install_path and Path(install_path).exists():
            import shutil
            shutil.rmtree(install_path)
        
        registry = RegistryManager()
        registry.uninstall_package(package, global_uninstall)
        print_success(f"Successfully uninstalled {package}")
        return 0
    except Exception as e:
        print_error(f"Error uninstalling package: {e}")
        return 1
