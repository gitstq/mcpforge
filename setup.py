#!/usr/bin/env python3
"""
MCPForge - Setup Script
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="mcpforge",
    version="1.0.0",
    description="Lightweight MCP Tool Package Manager CLI Engine",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="gitstq",
    author_email="",
    url="https://github.com/gitstq/mcpforge",
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.8",
    install_requires=[
        # Zero dependencies - using only standard library
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "mcpforge=mcpforge.cli:main",
            "mcpf=mcpforge.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Tools",
        "Topic :: Utilities",
    ],
    keywords="mcp model-context-protocol cli package-manager tools",
    project_urls={
        "Bug Reports": "https://github.com/gitstq/mcpforge/issues",
        "Source": "https://github.com/gitstq/mcpforge",
        "Documentation": "https://github.com/gitstq/mcpforge#readme",
    },
)
