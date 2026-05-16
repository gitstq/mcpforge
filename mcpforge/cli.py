#!/usr/bin/env python3
"""
MCPForge CLI - Main Command Line Interface
"""

import sys
import argparse
from typing import List, Optional

from mcpforge import __version__, __title__, __description__
from mcpforge.commands import (
    install_cmd,
    uninstall_cmd,
    list_cmd,
    search_cmd,
    info_cmd,
    init_cmd,
    validate_cmd,
    run_cmd,
    config_cmd,
    update_cmd,
)
from mcpforge.utils.colors import Colors
from mcpforge.utils.formatting import print_banner, print_version


def create_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(
        prog="mcpforge",
        description=f"{__title__} - {__description__}",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  mcpforge install @modelcontextprotocol/server-filesystem
  mcpforge search github
  mcpforge list
  mcpforge init my-mcp-server
  mcpforge validate ./my-server
  mcpforge run @modelcontextprotocol/server-filesystem

For more help: https://github.com/gitstq/mcpforge
        """
    )
    
    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"%(prog)s {__version__}"
    )
    
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable colored output"
    )
    
    parser.add_argument(
        "--verbose", "-V",
        action="store_true",
        help="Enable verbose output"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Install command
    install_parser = subparsers.add_parser(
        "install",
        aliases=["i", "add"],
        help="Install an MCP server or tool"
    )
    install_parser.add_argument(
        "package",
        help="Package name or URL to install"
    )
    install_parser.add_argument(
        "--global", "-g",
        action="store_true",
        dest="global_install",
        help="Install globally"
    )
    install_parser.add_argument(
        "--save", "-s",
        action="store_true",
        help="Save to mcpforge.json"
    )
    install_parser.set_defaults(func=install_cmd.execute)
    
    # Uninstall command
    uninstall_parser = subparsers.add_parser(
        "uninstall",
        aliases=["remove", "rm", "un"],
        help="Uninstall an MCP server or tool"
    )
    uninstall_parser.add_argument(
        "package",
        help="Package name to uninstall"
    )
    uninstall_parser.add_argument(
        "--global", "-g",
        action="store_true",
        dest="global_uninstall",
        help="Uninstall globally"
    )
    uninstall_parser.set_defaults(func=uninstall_cmd.execute)
    
    # List command
    list_parser = subparsers.add_parser(
        "list",
        aliases=["ls", "ll"],
        help="List installed MCP servers and tools"
    )
    list_parser.add_argument(
        "--global", "-g",
        action="store_true",
        dest="global_list",
        help="List global installations"
    )
    list_parser.add_argument(
        "--outdated", "-o",
        action="store_true",
        help="Show outdated packages"
    )
    list_parser.set_defaults(func=list_cmd.execute)
    
    # Search command
    search_parser = subparsers.add_parser(
        "search",
        aliases=["s", "find"],
        help="Search for MCP servers and tools"
    )
    search_parser.add_argument(
        "query",
        help="Search query"
    )
    search_parser.add_argument(
        "--limit", "-l",
        type=int,
        default=20,
        help="Maximum number of results (default: 20)"
    )
    search_parser.add_argument(
        "--source", "-S",
        choices=["npm", "github", "pypi", "all"],
        default="all",
        help="Search source"
    )
    search_parser.set_defaults(func=search_cmd.execute)
    
    # Info command
    info_parser = subparsers.add_parser(
        "info",
        aliases=["show", "view"],
        help="Show detailed information about a package"
    )
    info_parser.add_argument(
        "package",
        help="Package name"
    )
    info_parser.set_defaults(func=info_cmd.execute)
    
    # Init command
    init_parser = subparsers.add_parser(
        "init",
        aliases=["create", "new"],
        help="Initialize a new MCP server project"
    )
    init_parser.add_argument(
        "name",
        nargs="?",
        help="Project name"
    )
    init_parser.add_argument(
        "--template", "-t",
        choices=["python", "typescript", "javascript", "rust", "go"],
        default="python",
        help="Project template"
    )
    init_parser.add_argument(
        "--path", "-p",
        default=".",
        help="Project path"
    )
    init_parser.set_defaults(func=init_cmd.execute)
    
    # Validate command
    validate_parser = subparsers.add_parser(
        "validate",
        aliases=["check", "lint"],
        help="Validate an MCP server configuration"
    )
    validate_parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Path to validate"
    )
    validate_parser.add_argument(
        "--fix",
        action="store_true",
        help="Auto-fix issues when possible"
    )
    validate_parser.set_defaults(func=validate_cmd.execute)
    
    # Run command
    run_parser = subparsers.add_parser(
        "run",
        aliases=["start", "exec"],
        help="Run an MCP server"
    )
    run_parser.add_argument(
        "package",
        nargs="?",
        help="Package name to run"
    )
    run_parser.add_argument(
        "--config", "-c",
        help="Configuration file path"
    )
    run_parser.add_argument(
        "--transport",
        choices=["stdio", "sse", "http"],
        default="stdio",
        help="Transport type"
    )
    run_parser.add_argument(
        "--port", "-P",
        type=int,
        default=3000,
        help="Port for HTTP/SSE transport"
    )
    run_parser.set_defaults(func=run_cmd.execute)
    
    # Config command
    config_parser = subparsers.add_parser(
        "config",
        aliases=["cfg", "setting"],
        help="Manage MCPForge configuration"
    )
    config_subparsers = config_parser.add_subparsers(dest="config_action")
    
    config_get = config_subparsers.add_parser("get", help="Get configuration value")
    config_get.add_argument("key", help="Configuration key")
    config_get.set_defaults(func=config_cmd.get)
    
    config_set = config_subparsers.add_parser("set", help="Set configuration value")
    config_set.add_argument("key", help="Configuration key")
    config_set.add_argument("value", help="Configuration value")
    config_set.set_defaults(func=config_cmd.set)
    
    config_list = config_subparsers.add_parser("list", help="List all configuration")
    config_list.set_defaults(func=config_cmd.list_all)
    
    # Update command
    update_parser = subparsers.add_parser(
        "update",
        aliases=["upgrade", "up"],
        help="Update installed packages"
    )
    update_parser.add_argument(
        "package",
        nargs="?",
        help="Package to update (omit to update all)"
    )
    update_parser.add_argument(
        "--global", "-g",
        action="store_true",
        dest="global_update",
        help="Update global packages"
    )
    update_parser.set_defaults(func=update_cmd.execute)
    
    return parser


def main(args: Optional[List[str]] = None) -> int:
    """Main entry point for the CLI."""
    parser = create_parser()
    parsed_args = parser.parse_args(args)
    
    # Disable colors if requested
    if parsed_args.no_color:
        Colors.disable()
    
    # Show banner for main command
    if not parsed_args.command:
        print_banner()
        parser.print_help()
        return 0
    
    # Execute the command
    try:
        return parsed_args.func(parsed_args) or 0
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}⚠️  Operation cancelled by user{Colors.RESET}")
        return 130
    except Exception as e:
        print(f"{Colors.RED}❌ Error: {e}{Colors.RESET}")
        if parsed_args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
