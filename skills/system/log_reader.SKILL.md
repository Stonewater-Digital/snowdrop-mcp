---
skill: log_reader
category: system
description: Read recent log lines from a journalctl user-service or a local log file. For journalctl, provide service_name (e.g.
tier: free
inputs: source
---

# Log Reader

## Description
Read recent log lines from a journalctl user-service or a local log file. For journalctl, provide service_name (e.g. 'snowdrop-mcp'). For file, provide file_path (absolute path). Optionally specify lines (default 50) and, for journalctl, a since expression such as '1 hour ago' or 'today'.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `source` | `string` | Yes | Log source: 'journalctl' or 'file'. |
| `service_name` | `string` | No | Systemd user service name (required when source='journalctl'). |
| `file_path` | `string` | No | Absolute path to log file (required when source='file'). |
| `lines` | `integer` | No | Number of recent lines to return (default 50, max 2000). |
| `since` | `string` | No | journalctl --since expression, e.g. '1 hour ago' or 'today'. Only used when source='journalctl'. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "log_reader",
  "arguments": {
    "source": "<source>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "log_reader"`.
