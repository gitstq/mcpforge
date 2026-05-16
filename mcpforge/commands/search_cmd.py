#!/usr/bin/env python3
"""
Search Command - Search for MCP servers and tools
"""

import json
import urllib.request
import urllib.error
from argparse import Namespace
from typing import List, Dict, Any

from mcpforge.utils.formatting import print_table, print_info, print_error, print_package_info
from mcpforge.utils.colors import Colors


def execute(args: Namespace) -> int:
    """Execute the search command."""
    query = args.query
    limit = args.limit
    source = args.source
    
    print_info(f"Searching for '{query}'...")
    
    results = []
    
    if source in ["npm", "all"]:
        npm_results = search_npm(query, limit)
        results.extend(npm_results)
    
    if source in ["github", "all"]:
        github_results = search_github(query, limit)
        results.extend(github_results)
    
    if source in ["pypi", "all"]:
        pypi_results = search_pypi(query, limit)
        results.extend(pypi_results)
    
    if not results:
        print_info(f"No results found for '{query}'")
        return 0
    
    # Display results
    print()
    headers = ["Name", "Description", "Source"]
    rows = []
    
    for pkg in results[:limit]:
        name = pkg.get("name", "Unknown")
        desc = pkg.get("description", "No description")
        if len(desc) > 50:
            desc = desc[:47] + "..."
        src = pkg.get("source", "unknown")
        
        rows.append([
            Colors.colorize(name, Colors.BRIGHT_CYAN),
            desc,
            Colors.colorize(src, Colors.YELLOW)
        ])
    
    print_table(headers, rows)
    print()
    print(f"Found {len(results)} result(s). Showing first {min(len(results), limit)}.")
    print(f"Run 'mcpforge info <package>' for more details.")
    
    return 0


def search_npm(query: str, limit: int) -> List[Dict[str, Any]]:
    """Search NPM registry."""
    results = []
    try:
        # Search for MCP-related packages
        url = f"https://registry.npmjs.org/-/v1/search?text={query}+mcp&size={limit}"
        req = urllib.request.Request(url, headers={"Accept": "application/json"})
        
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            
            for pkg in data.get("objects", []):
                package = pkg.get("package", {})
                results.append({
                    "name": package.get("name", ""),
                    "description": package.get("description", "No description"),
                    "version": package.get("version", "unknown"),
                    "source": "npm",
                    "homepage": package.get("links", {}).get("homepage", ""),
                    "repository": package.get("links", {}).get("repository", ""),
                })
    except Exception as e:
        pass  # Silently fail for now
    
    return results


def search_github(query: str, limit: int) -> List[Dict[str, Any]]:
    """Search GitHub for MCP repositories."""
    results = []
    try:
        # Use GitHub search API
        search_query = f"{query}+mcp+language:python+language:typescript+language:javascript"
        url = f"https://api.github.com/search/repositories?q={search_query}&sort=stars&order=desc&per_page={limit}"
        req = urllib.request.Request(url, headers={
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "MCPForge"
        })
        
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            
            for repo in data.get("items", []):
                results.append({
                    "name": repo.get("full_name", ""),
                    "description": repo.get("description", "No description"),
                    "version": f"⭐ {repo.get('stargazers_count', 0)}",
                    "source": "github",
                    "homepage": repo.get("homepage", ""),
                    "repository": repo.get("html_url", ""),
                })
    except Exception as e:
        pass  # Silently fail for now
    
    return results


def search_pypi(query: str, limit: int) -> List[Dict[str, Any]]:
    """Search PyPI for MCP packages."""
    results = []
    try:
        # PyPI search API
        url = f"https://pypi.org/search/?q={query}+mcp"
        # Note: PyPI doesn't have a simple JSON search API
        # This is a placeholder for future implementation
    except Exception as e:
        pass
    
    return results
