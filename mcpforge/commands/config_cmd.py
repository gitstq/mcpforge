#!/usr/bin/env python3
"""
Config Command - Manage MCPForge configuration
"""

from argparse import Namespace

from mcpforge.utils.formatting import print_success, print_error, print_info
from mcpforge.utils.config import get_config
from mcpforge.utils.colors import Colors


def get(args: Namespace) -> int:
    """Get a configuration value."""
    key = args.key
    config = get_config()
    
    value = config.get(key)
    if value is not None:
        print(f"{Colors.CYAN}{key}{Colors.RESET} = {Colors.GREEN}{value}{Colors.RESET}")
        return 0
    else:
        print_error(f"Configuration key '{key}' not found")
        return 1


def set(args: Namespace) -> int:
    """Set a configuration value."""
    key = args.key
    value = args.value
    config = get_config()
    
    # Try to convert value to appropriate type
    if value.lower() in ("true", "yes", "1"):
        value = True
    elif value.lower() in ("false", "no", "0"):
        value = False
    elif value.isdigit():
        value = int(value)
    
    config.set(key, value)
    print_success(f"Set {key} = {value}")
    return 0


def list_all(args: Namespace) -> int:
    """List all configuration values."""
    config = get_config()
    settings = config.get_all()
    
    print()
    print(f"{Colors.BOLD}Configuration Settings:{Colors.RESET}")
    print(f"{Colors.DIM}{'─' * 50}{Colors.RESET}")
    
    for key, value in sorted(settings.items()):
        print(f"  {Colors.CYAN}{key:<30}{Colors.RESET} {Colors.GREEN}{value}{Colors.RESET}")
    
    print()
    print(f"Config file: {Colors.DIM}{config.CONFIG_FILE}{Colors.RESET}")
    return 0
