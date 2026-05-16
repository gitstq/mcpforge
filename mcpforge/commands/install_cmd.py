#!/usr/bin/env python3
"""
Install Command - Install MCP servers and tools
"""

import os
import subprocess
import json
from pathlib import Path
from argparse import Namespace

from mcpforge.utils.formatting import print_success, print_error, print_info, print_warning
from mcpforge.utils.registry import RegistryManager


def execute(args: Namespace) -> int:
    """Execute the install command."""
    package = args.package
    global_install = args.global_install
    save = args.save
    
    print_info(f"Installing {package}...")
    
    # Determine package source
    if package.startswith("@") or "/" in package:
        # NPM package
        return install_npm(package, global_install, save)
    elif package.startswith("pypi:") or package.startswith("pip:"):
        # PyPI package
        pip_package = package.split(":", 1)[1]
        return install_pip(pip_package, global_install, save)
    elif package.startswith("gh:") or package.startswith("github:"):
        # GitHub repository
        repo = package.split(":", 1)[1]
        return install_github(repo, global_install, save)
    else:
        # Try to detect source
        print_info("Detecting package source...")
        # Default to npm for now
        return install_npm(package, global_install, save)


def install_npm(package: str, global_install: bool, save: bool) -> int:
    """Install an NPM package."""
    try:
        cmd = ["npm", "install"]
        if global_install:
            cmd.append("-g")
        cmd.append(package)
        
        print_info(f"Running: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print_success(f"Successfully installed {package}")
            
            # Register in MCPForge
            registry = RegistryManager()
            install_path = str(Path.home() / ".mcpforge" / "global" if global_install else ".mcpforge/packages")
            registry.install_package(
                name=package,
                version="latest",
                source="npm",
                install_path=install_path,
                global_install=global_install
            )
            
            if save and not global_install:
                save_to_mcpforge_json(package, "npm")
            
            return 0
        else:
            print_error(f"Failed to install {package}")
            if result.stderr:
                print(result.stderr)
            return 1
    except FileNotFoundError:
        print_error("npm not found. Please install Node.js and npm.")
        return 1
    except Exception as e:
        print_error(f"Error installing package: {e}")
        return 1


def install_pip(package: str, global_install: bool, save: bool) -> int:
    """Install a PyPI package."""
    try:
        cmd = ["pip", "install"]
        if global_install:
            cmd.append("--user")
        cmd.append(package)
        
        print_info(f"Running: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print_success(f"Successfully installed {package}")
            
            registry = RegistryManager()
            install_path = str(Path.home() / ".local" / "lib" / "python" / "site-packages")
            registry.install_package(
                name=package,
                version="latest",
                source="pypi",
                install_path=install_path,
                global_install=global_install
            )
            
            if save and not global_install:
                save_to_mcpforge_json(package, "pypi")
            
            return 0
        else:
            print_error(f"Failed to install {package}")
            if result.stderr:
                print(result.stderr)
            return 1
    except FileNotFoundError:
        print_error("pip not found. Please install Python and pip.")
        return 1
    except Exception as e:
        print_error(f"Error installing package: {e}")
        return 1


def install_github(repo: str, global_install: bool, save: bool) -> int:
    """Install from GitHub repository."""
    try:
        # Clone the repository
        clone_dir = Path.home() / ".mcpforge" / "github" / repo.replace("/", "-")
        if clone_dir.exists():
            print_warning(f"Directory {clone_dir} already exists. Pulling latest changes...")
            result = subprocess.run(
                ["git", "-C", str(clone_dir), "pull"],
                capture_output=True,
                text=True
            )
        else:
            clone_dir.parent.mkdir(parents=True, exist_ok=True)
            result = subprocess.run(
                ["git", "clone", f"https://github.com/{repo}.git", str(clone_dir)],
                capture_output=True,
                text=True
            )
        
        if result.returncode == 0:
            print_success(f"Successfully cloned {repo}")
            
            # Try to install dependencies
            if (clone_dir / "package.json").exists():
                print_info("Installing NPM dependencies...")
                subprocess.run(["npm", "install"], cwd=clone_dir, capture_output=True)
            elif (clone_dir / "requirements.txt").exists():
                print_info("Installing Python dependencies...")
                subprocess.run(["pip", "install", "-r", "requirements.txt"], cwd=clone_dir, capture_output=True)
            
            # Register in MCPForge
            registry = RegistryManager()
            registry.install_package(
                name=repo,
                version="git",
                source="github",
                install_path=str(clone_dir),
                global_install=global_install
            )
            
            if save and not global_install:
                save_to_mcpforge_json(repo, "github")
            
            return 0
        else:
            print_error(f"Failed to clone {repo}")
            if result.stderr:
                print(result.stderr)
            return 1
    except FileNotFoundError:
        print_error("git not found. Please install Git.")
        return 1
    except Exception as e:
        print_error(f"Error cloning repository: {e}")
        return 1


def save_to_mcpforge_json(package: str, source: str):
    """Save package to mcpforge.json."""
    mcpforge_file = Path("mcpforge.json")
    
    data = {}
    if mcpforge_file.exists():
        with open(mcpforge_file, 'r') as f:
            data = json.load(f)
    
    if "dependencies" not in data:
        data["dependencies"] = {}
    
    data["dependencies"][package] = f"{source}:latest"
    
    with open(mcpforge_file, 'w') as f:
        json.dump(data, f, indent=2)
    
    print_success(f"Saved {package} to mcpforge.json")
