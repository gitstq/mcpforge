#!/usr/bin/env python3
"""
Tests for colors utility
"""

import unittest
from mcpforge.utils.colors import Colors


class TestColors(unittest.TestCase):
    """Test cases for Colors class."""
    
    def test_colorize_enabled(self):
        """Test colorize when colors are enabled."""
        Colors.enable()
        result = Colors.colorize("test", Colors.RED)
        self.assertIn(Colors.RED, result)
        self.assertIn(Colors.RESET, result)
    
    def test_colorize_disabled(self):
        """Test colorize when colors are disabled."""
        Colors.disable()
        result = Colors.colorize("test", Colors.RED)
        self.assertEqual(result, "test")
        Colors.enable()
    
    def test_strip_colors(self):
        """Test stripping colors from text."""
        colored = f"{Colors.RED}test{Colors.RESET}"
        result = Colors.strip(colored)
        self.assertEqual(result, "test")


if __name__ == "__main__":
    unittest.main()
