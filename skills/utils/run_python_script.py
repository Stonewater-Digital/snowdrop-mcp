import os
import subprocess
from typing import Dict, Any

TOOL_META = {
    "name": "run_python_script",
    "description": "Executes a Python script within the project context, automatically handling PYTHONPATH and virtual environment activation to prevent ModuleNotFound errors.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "script_path": {
                "type": "string",
                "description": "Relative path to the Python script from the project root (e.g., 'scripts/my_script.py')"
            },
            "args": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Optional list of arguments to pass to the script"
            }
        },
        "required": ["script_path"]
    }
}

def run_python_script(script_path: str, args: list[str] = None, **kwargs) -> Dict[str, Any]:
    """Execute a python script correctly using venv and PYTHONPATH."""
    args = args or []
    
    # Determine absolute project root (assuming this skill is in skills/utils/)
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    
    # Construct paths
    venv_python = os.path.join(project_root, "venv", "bin", "python")
    if not os.path.exists(venv_python):
        # Fallback to system python if venv doesn't exist
        venv_python = "python3"
        
    full_script_path = os.path.join(project_root, script_path)
    
    if not os.path.exists(full_script_path):
        return {"status": "error", "message": f"Script not found: {full_script_path}"}
        
    # Setup environment with PYTHONPATH
    env = os.environ.copy()
    env["PYTHONPATH"] = project_root
    
    command = [venv_python, full_script_path] + args
    
    try:
        result = subprocess.run(
            command,
            env=env,
            cwd=project_root,
            capture_output=True,
            text=True,
            check=False
        )
        
        if result.returncode == 0:
            return {
                "status": "success",
                "stdout": result.stdout,
                "stderr": result.stderr
            }
        else:
            return {
                "status": "error",
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode
            }
            
    except Exception as e:
        return {"status": "error", "message": str(e)}
