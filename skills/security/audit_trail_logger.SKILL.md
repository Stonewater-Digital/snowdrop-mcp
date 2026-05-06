---
skill: audit_trail_logger
category: security
description: Writes immutable audit entries to logs/audit_trail.jsonl.
tier: free
inputs: action, actor, details, previous_hash
---

# Audit Trail Logger

## Description
Writes immutable audit entries to logs/audit_trail.jsonl.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `action` | `string` | Yes |  |
| `actor` | `string` | Yes |  |
| `details` | `object` | Yes |  |
| `previous_hash` | `string` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "audit_trail_logger",
  "arguments": {
    "action": "<action>",
    "actor": "<actor>",
    "details": {},
    "previous_hash": "<previous_hash>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "audit_trail_logger"`.
