---
skill: support_ticket_manager
category: support
description: Creates, updates, closes, and lists support tickets with SLA tracking.
tier: free
inputs: operation
---

# Support Ticket Manager

## Description
Creates, updates, closes, and lists support tickets with SLA tracking.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `operation` | `string` | Yes |  |
| `ticket` | `['object', 'null']` | No |  |
| `ticket_id` | `['string', 'null']` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "support_ticket_manager",
  "arguments": {
    "operation": "<operation>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "support_ticket_manager"`.
