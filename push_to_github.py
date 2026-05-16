#!/usr/bin/env python3
"""
Push files to GitHub using API
"""

import os
import base64
import json
import urllib.request
import urllib.error
from pathlib import Path

TOKEN = os.environ.get("GH_TOKEN", "")
REPO = "gitstq/mcpforge"
API_BASE = f"https://api.github.com/repos/{REPO}"


def api_request(method, endpoint, data=None):
    """Make API request to GitHub."""
    url = f"{API_BASE}/{endpoint}"
    headers = {
        "Authorization": f"token {TOKEN}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "MCPForge",
        "Content-Type": "application/json"
    }
    
    req = urllib.request.Request(url, method=method, headers=headers)
    if data:
        req.data = json.dumps(data).encode('utf-8')
    
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        print(f"Error: {e.code} - {e.read().decode()}")
        return None


def create_or_update_file(path, content, message, sha=None):
    """Create or update a file in the repository."""
    endpoint = f"contents/{path}"
    data = {
        "message": message,
        "content": base64.b64encode(content.encode()).decode()
    }
    if sha:
        data["sha"] = sha
    
    return api_request("PUT", endpoint, data)


def get_file_sha(path):
    """Get SHA of existing file."""
    result = api_request("GET", f"contents/{path}")
    if result and "sha" in result:
        return result["sha"]
    return None


def upload_directory(local_path, repo_path=""):
    """Upload directory contents to GitHub."""
    local_path = Path(local_path)
    
    for item in local_path.iterdir():
        if item.name.startswith('.') and item.name != '.gitignore':
            continue
        if item.name == '__pycache__':
            continue
        
        relative_path = f"{repo_path}/{item.name}" if repo_path else item.name
        
        if item.is_dir():
            upload_directory(item, relative_path)
        else:
            content = item.read_text(encoding='utf-8', errors='ignore')
            sha = get_file_sha(relative_path)
            
            message = f"Add {relative_path}" if not sha else f"Update {relative_path}"
            result = create_or_update_file(relative_path, content, message, sha)
            
            if result:
                print(f"✓ {relative_path}")
            else:
                print(f"✗ {relative_path}")


if __name__ == "__main__":
    print("Uploading files to GitHub...")
    upload_directory("/data/user/work/mcpforge")
    print("Done!")
