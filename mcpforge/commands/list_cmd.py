#!/usr/bin/env python3
"""
List Command - List installed MCP servers and tools
"""

from argparse import Namespace
from typing import List, Dict, Any

from mcpforge.utils.formatting import print_table, print_info, print_warning
from mcpforge.utils.registry import RegistryManager
from mcpforge.utils.colors import Colors


def execute(args: Namespace) -> int:
    """Execute the list command."""
    global_list = args.global_list
    outdated = args.outdated
    
    registry = RegistryManager()
    packages = registry.list_packages(global_only=global_list)
    
    if not packages:
        if global_list:
            print_info("No globally installed packages found.")
        else:
            print_info("No installed packages found. Run 'mcpforge install <package>' to install one.")
        return 0
    
    if outdated:
        packages = [p for p in packages if is_outdated(p)]
        if not packages:
            print_info("All packages are up to date!")
            return 0
    
    # Prepare table data
    headers = ["Package", "Version", "Source", "Scope"]
    rows = []
    
    for pkg in packages:
        rows.append([
            pkg.get("name", "Unknown"),
            pkg.get("version", "unknown"),
            pkg.get("source", "unknown"),
            format_scope(pkg.get("scope", "local"))
        ])
    
    print()
    print_table(headers, rows)
    print()
    print(f"Total: {len(packages)} package(s)")
    
    return 0


def format_scope(scope: str) -> str:
    """Format scope with color."""
    if scope == "global":
        return Colors.colorize(scope, Colors.YELLOW)
    return Colors.colorize(scope, Colors.GREEN)


def is_outdated(package: Dict[str, Any]) -> bool:
    """Check if a package is outdated."""
    # This would check against the remote registry
    # For now, always return False
    return False
