#!/usr/bin/env python3
"""
Terminal Colors Utility
终端颜色工具
"""

import os
import sys


class Colors:
    """ANSI color codes for terminal output."""
    
    # Standard colors
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    
    # Bright colors
    BRIGHT_BLACK = "\033[90m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"
    
    # Background colors
    BG_BLACK = "\033[40m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"
    BG_WHITE = "\033[47m"
    
    # Styles
    BOLD = "\033[1m"
    DIM = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    BLINK = "\033[5m"
    REVERSE = "\033[7m"
    STRIKETHROUGH = "\033[9m"
    
    # Reset
    RESET = "\033[0m"
    
    _enabled = True
    
    @classmethod
    def disable(cls):
        """Disable all colors."""
        cls._enabled = False
    
    @classmethod
    def enable(cls):
        """Enable colors."""
        cls._enabled = True
    
    @classmethod
    def is_enabled(cls) -> bool:
        """Check if colors are enabled."""
        if not cls._enabled:
            return False
        # Check for NO_COLOR environment variable
        if os.environ.get("NO_COLOR"):
            return False
        # Check if output is a terminal
        if not sys.stdout.isatty():
            return False
        # Check TERM environment variable
        term = os.environ.get("TERM", "")
        if term == "dumb":
            return False
        return True
    
    @classmethod
    def colorize(cls, text: str, color: str) -> str:
        """Apply color to text if colors are enabled."""
        if cls.is_enabled():
            return f"{color}{text}{cls.RESET}"
        return text
    
    @classmethod
    def strip(cls, text: str) -> str:
        """Remove ANSI color codes from text."""
        import re
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        return ansi_escape.sub('', text)


def supports_unicode() -> bool:
    """Check if terminal supports Unicode characters."""
    try:
        # Try to encode a unicode character
        "✓".encode(sys.stdout.encoding or 'utf-8')
        return True
    except (UnicodeEncodeError, AttributeError):
        return False
