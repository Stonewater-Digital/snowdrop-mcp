---
skill: run_python_script
category: utils
description: Executes a Python script within the project context, automatically handling PYTHONPATH and virtual environment activation to prevent ModuleNotFound errors.
tier: free
inputs: script_path
---

# Run Python Script

## Description
Executes a Python script within the project context, automatically handling PYTHONPATH and virtual environment activation to prevent ModuleNotFound errors.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `script_path` | `string` | Yes | Relative path to the Python script from the project root (e.g., 'scripts/my_script.py') |
| `args` | `array` | No | Optional list of arguments to pass to the script |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "run_python_script",
  "arguments": {
    "script_path": "<script_path>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "run_python_script"`.
