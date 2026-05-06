---
skill: sheet_pruner
category: social
description: Prevents data bloat by autonomously removing logs older than the retention period from the Command Center.
tier: free
inputs: none
---

# Sheet Pruner

## Description
Prevents data bloat by autonomously removing logs older than the retention period from the Command Center.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `retention_days` | `integer` | No | Number of days to keep data. Defaults to 7. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "sheet_pruner",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "sheet_pruner"`.
