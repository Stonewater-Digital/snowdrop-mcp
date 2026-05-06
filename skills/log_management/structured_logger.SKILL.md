---
skill: structured_logger
category: log_management
description: Appends structured log entries with correlation metadata to a JSONL file.
tier: free
inputs: level, message
---

# Structured Logger

## Description
Appends structured log entries with correlation metadata to a JSONL file.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `level` | `string` | Yes |  |
| `message` | `string` | Yes |  |
| `context` | `object` | No |  |
| `log_file` | `string` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "structured_logger",
  "arguments": {
    "level": "<level>",
    "message": "<message>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "structured_logger"`.
