---
skill: support_escalation_router
category: support
description: Determines routing paths for support tickets based on category, tier, and urgency.
tier: free
inputs: ticket
---

# Support Escalation Router

## Description
Determines routing paths for support tickets based on category, tier, and urgency.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `ticket` | `object` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "support_escalation_router",
  "arguments": {
    "ticket": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "support_escalation_router"`.
