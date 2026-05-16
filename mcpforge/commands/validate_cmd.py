#!/usr/bin/env python3
"""
Validate Command - Validate MCP server configuration
"""

import json
from pathlib import Path
from argparse import Namespace

from mcpforge.utils.formatting import print_success, print_error, print_info, print_warning
from mcpforge.utils.colors import Colors


def execute(args: Namespace) -> int:
    """Execute the validate command."""
    path = args.path
    auto_fix = args.fix
    
    print_info(f"Validating MCP server at: {path}")
    
    project_path = Path(path)
    
    if not project_path.exists():
        print_error(f"Path does not exist: {path}")
        return 1
    
    issues = []
    warnings = []
    
    # Check for mcpforge.json
    mcpforge_file = project_path / "mcpforge.json"
    if mcpforge_file.exists():
        try:
            with open(mcpforge_file, 'r') as f:
                config = json.load(f)
            
            # Validate required fields
            if "name" not in config:
                issues.append("Missing 'name' in mcpforge.json")
            if "version" not in config:
                issues.append("Missing 'version' in mcpforge.json")
            if "type" not in config:
                warnings.append("Missing 'type' in mcpforge.json")
            
            print_success("mcpforge.json is valid")
        except json.JSONDecodeError as e:
            issues.append(f"Invalid JSON in mcpforge.json: {e}")
    else:
        warnings.append("No mcpforge.json found")
    
    # Check for package files based on project type
    if (project_path / "package.json").exists():
        issues.extend(validate_node_project(project_path))
    elif (project_path / "pyproject.toml").exists() or (project_path / "setup.py").exists():
        issues.extend(validate_python_project(project_path))
    else:
        warnings.append("No package.json or pyproject.toml found")
    
    # Check for README
    if not (project_path / "README.md").exists():
        warnings.append("No README.md found")
    
    # Check for LICENSE
    if not list(project_path.glob("LICENSE*")):
        warnings.append("No LICENSE file found")
    
    # Print results
    print()
    if issues:
        print_error(f"Found {len(issues)} issue(s):")
        for issue in issues:
            print(f"  {Colors.RED}✗{Colors.RESET} {issue}")
    
    if warnings:
        print_warning(f"Found {len(warnings)} warning(s):")
        for warning in warnings:
            print(f"  {Colors.YELLOW}⚠{Colors.RESET} {warning}")
    
    if not issues and not warnings:
        print_success("Validation passed! No issues found.")
        return 0
    elif not issues:
        print_warning("Validation passed with warnings.")
        return 0
    else:
        print_error("Validation failed.")
        return 1


def validate_node_project(project_path: Path) -> list:
    """Validate a Node.js project."""
    issues = []
    
    try:
        with open(project_path / "package.json", 'r') as f:
            pkg = json.load(f)
        
        if "name" not in pkg:
            issues.append("Missing 'name' in package.json")
        if "version" not in pkg:
            issues.append("Missing 'version' in package.json")
        if "dependencies" not in pkg and "devDependencies" not in pkg:
            issues.append("No dependencies found in package.json")
        
        # Check for MCP SDK
        deps = pkg.get("dependencies", {})
        if "@modelcontextprotocol/sdk" not in deps:
            warnings.append("@modelcontextprotocol/sdk not in dependencies")
        
    except json.JSONDecodeError as e:
        issues.append(f"Invalid JSON in package.json: {e}")
    except Exception as e:
        issues.append(f"Error reading package.json: {e}")
    
    return issues


def validate_python_project(project_path: Path) -> list:
    """Validate a Python project."""
    issues = []
    
    # Check for pyproject.toml
    pyproject_file = project_path / "pyproject.toml"
    if pyproject_file.exists():
        try:
            content = pyproject_file.read_text()
            if "[project]" not in content:
                issues.append("Missing [project] section in pyproject.toml")
            if "name" not in content:
                issues.append("Missing 'name' in pyproject.toml")
        except Exception as e:
            issues.append(f"Error reading pyproject.toml: {e}")
    
    # Check for requirements.txt or similar
    req_file = project_path / "requirements.txt"
    if req_file.exists():
        content = req_file.read_text()
        if "mcp" not in content.lower():
            warnings.append("mcp package not found in requirements.txt")
    
    return issues
