import os
import subprocess
from typing import Dict, Any

TOOL_META = {
    "name": "multi_repo_executor",
    "description": "Executes a shell command across all Stonewater-Digital repositories locally, handling cloning/pulling if necessary.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "command": {
                "type": "string",
                "description": "The shell command to execute in each repository (e.g., 'git status')"
            }
        },
        "required": ["command"]
    }
}

REPOS = [
    "snowdrop-core",
    "snowdrop-mcp",
    "the-watering-hole"
]

def multi_repo_executor(command: str, **kwargs) -> Dict[str, Any]:
    """Execute a command across all known organization repositories."""
    # Base directory for all repos
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    
    results = {}
    
    for repo in REPOS:
        repo_path = os.path.join(base_dir, repo)
        
        # If repo is not in the base dir, check tmp_repos (where we cloned some)
        if not os.path.exists(repo_path):
            repo_path = os.path.join(base_dir, "snowdrop-core", "tmp_repos", repo)
            
        if not os.path.exists(repo_path):
            results[repo] = {"status": "error", "message": "Repository not cloned locally."}
            continue
            
        try:
            process = subprocess.run(
                command,
                shell=True,
                cwd=repo_path,
                capture_output=True,
                text=True
            )
            
            results[repo] = {
                "status": "success" if process.returncode == 0 else "error",
                "returncode": process.returncode,
                "stdout": process.stdout.strip(),
                "stderr": process.stderr.strip()
            }
        except Exception as e:
            results[repo] = {"status": "error", "message": str(e)}
            
    return {"status": "completed", "results": results}
