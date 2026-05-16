#!/usr/bin/env python3
"""
Formatting Utilities for MCPForge
"""

import shutil
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime

from mcpforge import __version__, __title__
from .colors import Colors


def get_terminal_width() -> int:
    """Get terminal width, defaulting to 80 if not available."""
    try:
        return shutil.get_terminal_size().columns
    except:
        return 80


def print_banner():
    """Print the MCPForge banner."""
    banner = f"""
{Colors.CYAN}╔═══════════════════════════════════════════════════════════════╗{Colors.RESET}
{Colors.CYAN}║{Colors.RESET}  {Colors.BOLD}{Colors.BRIGHT_CYAN}🔧 MCPForge{Colors.RESET}                                                    {Colors.CYAN}║{Colors.RESET}
{Colors.CYAN}║{Colors.RESET}  {Colors.DIM}Lightweight MCP Tool Package Manager CLI{Colors.RESET}                     {Colors.CYAN}║{Colors.RESET}
{Colors.CYAN}║{Colors.RESET}  {Colors.DIM}Version {__version__}{Colors.RESET}                                                  {Colors.CYAN}║{Colors.RESET}
{Colors.CYAN}╚═══════════════════════════════════════════════════════════════╝{Colors.RESET}
"""
    print(banner)


def print_version():
    """Print version information."""
    print(f"{__title__} version {__version__}")


def print_success(message: str):
    """Print a success message."""
    print(f"{Colors.GREEN}✓ {message}{Colors.RESET}")


def print_error(message: str):
    """Print an error message."""
    print(f"{Colors.RED}✗ {message}{Colors.RESET}")


def print_warning(message: str):
    """Print a warning message."""
    print(f"{Colors.YELLOW}⚠ {message}{Colors.RESET}")


def print_info(message: str):
    """Print an info message."""
    print(f"{Colors.BLUE}ℹ {message}{Colors.RESET}")


def print_table(
    headers: List[str],
    rows: List[List[Any]],
    max_width: Optional[int] = None
) -> str:
    """
    Print a formatted table.
    
    Args:
        headers: List of column headers
        rows: List of row data
        max_width: Maximum width for the table
    """
    if not rows:
        return "No data to display."
    
    if max_width is None:
        max_width = get_terminal_width() - 4
    
    # Calculate column widths
    col_widths = []
    for i, header in enumerate(headers):
        max_col_width = len(str(header))
        for row in rows:
            if i < len(row):
                max_col_width = max(max_col_width, len(str(row[i])))
        col_widths.append(min(max_col_width, max_width // len(headers)))
    
    # Build table
    lines = []
    
    # Top border
    top = "┌" + "┬".join("─" * (w + 2) for w in col_widths) + "┐"
    lines.append(Colors.colorize(top, Colors.CYAN))
    
    # Header row
    header_row = "│"
    for i, header in enumerate(headers):
        cell = f" {str(header)[:col_widths[i]].ljust(col_widths[i])} "
        header_row += Colors.colorize(cell, Colors.BOLD + Colors.BRIGHT_CYAN) + "│"
    lines.append(header_row)
    
    # Separator
    sep = "├" + "┼".join("─" * (w + 2) for w in col_widths) + "┤"
    lines.append(Colors.colorize(sep, Colors.CYAN))
    
    # Data rows
    for row in rows:
        data_row = "│"
        for i in range(len(headers)):
            if i < len(row):
                cell_text = str(row[i])[:col_widths[i]].ljust(col_widths[i])
            else:
                cell_text = " " * col_widths[i]
            cell = f" {cell_text} "
            data_row += cell + "│"
        lines.append(data_row)
    
    # Bottom border
    bottom = "└" + "┴".join("─" * (w + 2) for w in col_widths) + "┘"
    lines.append(Colors.colorize(bottom, Colors.CYAN))
    
    result = "\n".join(lines)
    print(result)
    return result


def format_size(size_bytes: int) -> str:
    """Format byte size to human readable string."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} PB"


def format_date(date_str: str) -> str:
    """Format date string to human readable format."""
    try:
        # Try ISO format
        dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        return dt.strftime("%Y-%m-%d %H:%M")
    except:
        try:
            # Try other common formats
            dt = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
            return dt.strftime("%Y-%m-%d %H:%M")
        except:
            return date_str


def format_duration(seconds: float) -> str:
    """Format duration in seconds to human readable string."""
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f}m"
    else:
        hours = seconds / 3600
        return f"{hours:.1f}h"


def truncate_text(text: str, max_length: int, suffix: str = "...") -> str:
    """Truncate text to maximum length."""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def progress_bar(
    current: int,
    total: int,
    width: int = 40,
    prefix: str = "",
    suffix: str = ""
) -> str:
    """Create a progress bar string."""
    if total == 0:
        return ""
    
    filled = int(width * current / total)
    bar = "█" * filled + "░" * (width - filled)
    percentage = 100 * current / total
    
    return f"{prefix} {Colors.colorize(bar, Colors.GREEN)} {percentage:.1f}% {suffix}"


def print_package_info(package: Dict[str, Any]):
    """Print detailed package information."""
    print()
    print(f"{Colors.BOLD}{Colors.BRIGHT_CYAN}{package.get('name', 'Unknown')}{Colors.RESET}")
    print(f"{Colors.DIM}{'─' * 60}{Colors.RESET}")
    
    if 'description' in package:
        print(f"{Colors.WHITE}{package['description']}{Colors.RESET}")
        print()
    
    info_lines = []
    if 'version' in package:
        info_lines.append(f"{Colors.CYAN}Version:{Colors.RESET} {package['version']}")
    if 'author' in package:
        info_lines.append(f"{Colors.CYAN}Author:{Colors.RESET} {package['author']}")
    if 'license' in package:
        info_lines.append(f"{Colors.CYAN}License:{Colors.RESET} {package['license']}")
    if 'homepage' in package:
        info_lines.append(f"{Colors.CYAN}Homepage:{Colors.RESET} {package['homepage']}")
    
    for line in info_lines:
        print(f"  {line}")
    
    if 'keywords' in package and package['keywords']:
        print()
        keywords = ', '.join(package['keywords'][:10])
        print(f"{Colors.CYAN}Keywords:{Colors.RESET} {Colors.colorize(keywords, Colors.YELLOW)}")
    
    print()
