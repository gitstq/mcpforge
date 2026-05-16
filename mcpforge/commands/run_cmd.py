#!/usr/bin/env python3
"""
Run Command - Run an MCP server
"""

import os
import subprocess
import json
from pathlib import Path
from argparse import Namespace

from mcpforge.utils.formatting import print_success, print_error, print_info, print_warning
from mcpforge.utils.registry import RegistryManager


def execute(args: Namespace) -> int:
    """Execute the run command."""
    package = args.package
    config_file = args.config
    transport = args.transport
    port = args.port
    
    # If no package specified, try to run from current directory
    if not package:
        return run_local(config_file, transport, port)
    
    # Get package info from registry
    registry = RegistryManager()
    pkg_info = registry.get_package(package)
    
    if not pkg_info:
        print_error(f"Package '{package}' is not installed")
        print_info(f"Run 'mcpforge install {package}' to install it")
        return 1
    
    install_path = pkg_info.get("install_path", "")
    source = pkg_info.get("source", "unknown")
    
    print_info(f"Running {package} from {install_path}")
    
    # Run based on source type
    if source == "npm":
        return run_npm_package(package, install_path, transport, port)
    elif source == "pypi":
        return run_pip_package(package, transport, port)
    elif source == "github":
        return run_github_package(package, install_path, transport, port)
    else:
        print_error(f"Unknown package source: {source}")
        return 1


def run_local(config_file: str, transport: str, port: int) -> int:
    """Run MCP server from current directory."""
    # Check for mcpforge.json
    mcpforge_file = Path("mcpforge.json")
    if not mcpforge_file.exists():
        print_error("No mcpforge.json found in current directory")
        print_info("Run 'mcpforge init' to create a new MCP server project")
        return 1
    
    try:
        with open(mcpforge_file, 'r') as f:
            config = json.load(f)
        
        template = config.get("template", "python")
        entry = config.get("entry", "")
        
        if template == "python":
            return run_python_entry(entry, transport, port)
        elif template in ["typescript", "javascript"]:
            return run_node_entry(entry, transport, port)
        else:
            print_error(f"Unknown template: {template}")
            return 1
            
    except json.JSONDecodeError as e:
        print_error(f"Invalid mcpforge.json: {e}")
        return 1
    except Exception as e:
        print_error(f"Error running local server: {e}")
        return 1


def run_npm_package(package: str, install_path: str, transport: str, port: int) -> int:
    """Run an NPM package."""
    try:
        # Try to run via npx
        cmd = ["npx", package]
        
        env = os.environ.copy()
        if transport != "stdio":
            env["MCP_TRANSPORT"] = transport
            env["MCP_PORT"] = str(port)
        
        print_info(f"Executing: {' '.join(cmd)}")
        result = subprocess.run(cmd, env=env)
        return result.returncode
        
    except FileNotFoundError:
        print_error("npx not found. Please install Node.js")
        return 1
    except Exception as e:
        print_error(f"Error running package: {e}")
        return 1


def run_pip_package(package: str, transport: str, port: int) -> int:
    """Run a PyPI package."""
    try:
        # Try to run as a module
        module_name = package.replace("-", "_")
        cmd = ["python", "-m", module_name]
        
        env = os.environ.copy()
        if transport != "stdio":
            env["MCP_TRANSPORT"] = transport
            env["MCP_PORT"] = str(port)
        
        print_info(f"Executing: {' '.join(cmd)}")
        result = subprocess.run(cmd, env=env)
        return result.returncode
        
    except Exception as e:
        print_error(f"Error running package: {e}")
        return 1


def run_github_package(package: str, install_path: str, transport: str, port: int) -> int:
    """Run a GitHub package."""
    install_path = Path(install_path)
    
    if not install_path.exists():
        print_error(f"Install path does not exist: {install_path}")
        return 1
    
    # Check for package.json
    if (install_path / "package.json").exists():
        return run_node_entry("index.js", transport, port, cwd=install_path)
    
    # Check for Python files
    py_files = list(install_path.glob("*.py"))
    if py_files:
        return run_python_entry(str(py_files[0]), transport, port)
    
    print_error("Could not determine how to run this package")
    return 1


def run_python_entry(entry: str, transport: str, port: int, cwd: str = None) -> int:
    """Run a Python entry point."""
    try:
        if ":" in entry:
            # Module:function format
            module, func = entry.split(":")
            cmd = ["python", "-m", module]
        else:
            # File path
            cmd = ["python", entry]
        
        env = os.environ.copy()
        if transport != "stdio":
            env["MCP_TRANSPORT"] = transport
            env["MCP_PORT"] = str(port)
        
        print_info(f"Executing: {' '.join(cmd)}")
        result = subprocess.run(cmd, env=env, cwd=cwd)
        return result.returncode
        
    except Exception as e:
        print_error(f"Error running Python entry: {e}")
        return 1


def run_node_entry(entry: str, transport: str, port: int, cwd: str = None) -> int:
    """Run a Node.js entry point."""
    try:
        cmd = ["node", entry]
        
        env = os.environ.copy()
        if transport != "stdio":
            env["MCP_TRANSPORT"] = transport
            env["MCP_PORT"] = str(port)
        
        print_info(f"Executing: {' '.join(cmd)}")
        result = subprocess.run(cmd, env=env, cwd=cwd)
        return result.returncode
        
    except FileNotFoundError:
        print_error("node not found. Please install Node.js")
        return 1
    except Exception as e:
        print_error(f"Error running Node.js entry: {e}")
        return 1
