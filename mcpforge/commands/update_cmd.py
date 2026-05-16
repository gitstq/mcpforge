#!/usr/bin/env python3
"""
Update Command - Update installed packages
"""

from argparse import Namespace

from mcpforge.utils.formatting import print_success, print_error, print_info, print_warning
from mcpforge.utils.registry import RegistryManager


def execute(args: Namespace) -> int:
    """Execute the update command."""
    package = args.package
    global_update = args.global_update
    
    registry = RegistryManager()
    
    if package:
        # Update specific package
        return update_package(package, global_update)
    else:
        # Update all packages
        packages = registry.list_packages(global_only=global_update)
        
        if not packages:
            print_info("No packages to update")
            return 0
        
        print_info(f"Updating {len(packages)} package(s)...")
        updated = 0
        failed = 0
        
        for pkg in packages:
            name = pkg.get("name", "")
            if update_package(name, global_update) == 0:
                updated += 1
            else:
                failed += 1
        
        print()
        print_success(f"Updated {updated} package(s)")
        if failed > 0:
            print_warning(f"Failed to update {failed} package(s)")
        
        return 0 if failed == 0 else 1


def update_package(package: str, global_update: bool) -> int:
    """Update a single package."""
    registry = RegistryManager()
    pkg_info = registry.get_package(package, global_only=global_update)
    
    if not pkg_info:
        print_error(f"Package '{package}' is not installed")
        return 1
    
    source = pkg_info.get("source", "unknown")
    current_version = pkg_info.get("version", "unknown")
    
    print_info(f"Updating {package} (current: {current_version})...")
    
    # For now, just reinstall the package
    # In a full implementation, this would check for updates first
    if source == "npm":
        from .install_cmd import install_npm
        return install_npm(package, global_update, save=False)
    elif source == "pypi":
        from .install_cmd import install_pip
        return install_pip(package, global_update, save=False)
    elif source == "github":
        from .install_cmd import install_github
        return install_github(package, global_update, save=False)
    else:
        print_warning(f"Unknown package source: {source}")
        return 1
