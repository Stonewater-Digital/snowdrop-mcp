---
skill: log_rotation_manager
category: log_management
description: Evaluates log files and proposes rotation/compression/deletion actions.
tier: free
inputs: log_files, current_date
---

# Log Rotation Manager

## Description
Evaluates log files and proposes rotation/compression/deletion actions.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `log_files` | `array` | Yes |  |
| `current_date` | `string` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "log_rotation_manager",
  "arguments": {
    "log_files": [],
    "current_date": "<current_date>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "log_rotation_manager"`.
