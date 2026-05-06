---
skill: self_audit_daily
category: ralph_wiggum
description: Compares planned vs executed actions, logs discrepancies, and triggers freezes if needed.
tier: free
inputs: planned_actions, executed_actions
---

# Self Audit Daily

## Description
Compares planned vs executed actions, logs discrepancies, and triggers freezes if needed.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `planned_actions` | `array` | Yes |  |
| `executed_actions` | `array` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "self_audit_daily",
  "arguments": {
    "planned_actions": [],
    "executed_actions": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "self_audit_daily"`.
