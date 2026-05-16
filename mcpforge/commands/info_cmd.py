#!/usr/bin/env python3
"""
Info Command - Show detailed information about a package
"""

import json
import urllib.request
from argparse import Namespace

from mcpforge.utils.formatting import print_package_info, print_info, print_error, print_warning
from mcpforge.utils.registry import RegistryManager


def execute(args: Namespace) -> int:
    """Execute the info command."""
    package = args.package
    
    # First check if installed
    registry = RegistryManager()
    installed_pkg = registry.get_package(package)
    
    if installed_pkg:
        print_info(f"Package '{package}' is installed:")
        print_package_info({
            "name": package,
            **installed_pkg
        })
        return 0
    
    # Try to fetch from registries
    print_info(f"Fetching information for '{package}'...")
    
    # Try NPM first
    npm_info = fetch_npm_info(package)
    if npm_info:
        print_package_info(npm_info)
        return 0
    
    # Try GitHub
    if "/" in package:
        github_info = fetch_github_info(package)
        if github_info:
            print_package_info(github_info)
            return 0
    
    print_error(f"Package '{package}' not found")
    return 1


def fetch_npm_info(package: str) -> dict:
    """Fetch package info from NPM registry."""
    try:
        url = f"https://registry.npmjs.org/{package}"
        req = urllib.request.Request(url, headers={"Accept": "application/json"})
        
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            
            latest = data.get("dist-tags", {}).get("latest", "unknown")
            version_info = data.get("versions", {}).get(latest, {})
            
            return {
                "name": data.get("name", package),
                "description": data.get("description", "No description available"),
                "version": latest,
                "author": str(version_info.get("author", "Unknown")),
                "license": data.get("license", "Unknown"),
                "homepage": version_info.get("homepage", ""),
                "keywords": data.get("keywords", []),
                "source": "npm",
            }
    except Exception as e:
        return None


def fetch_github_info(repo: str) -> dict:
    """Fetch repository info from GitHub."""
    try:
        url = f"https://api.github.com/repos/{repo}"
        req = urllib.request.Request(url, headers={
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "MCPForge"
        })
        
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            
            return {
                "name": data.get("full_name", repo),
                "description": data.get("description", "No description available"),
                "version": f"⭐ {data.get('stargazers_count', 0)} stars",
                "author": data.get("owner", {}).get("login", "Unknown"),
                "license": data.get("license", {}).get("name", "Unknown"),
                "homepage": data.get("homepage", data.get("html_url", "")),
                "keywords": data.get("topics", []),
                "source": "github",
            }
    except Exception as e:
        return None
