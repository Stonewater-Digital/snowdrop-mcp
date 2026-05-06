---
skill: shell_exec
category: system
description: Run a shell command on the local system and return stdout, stderr, and exit code. Only commands whose first token(s) match an approved allowlist are permitted.
tier: free
inputs: command
---

# Shell Exec

## Description
Run a shell command on the local system and return stdout, stderr, and exit code. Only commands whose first token(s) match an approved allowlist are permitted. Allowed prefixes: curl, wget, python3, python, git, systemctl --user, journalctl, ps, top, df, free, uptime, cat, ls, find.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `command` | `string` | Yes | The shell command to run. Must start with an approved prefix. |
| `timeout` | `integer` | No | Timeout in seconds before the command is killed (default 30). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "shell_exec",
  "arguments": {
    "command": "<command>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "shell_exec"`.
