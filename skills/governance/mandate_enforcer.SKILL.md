---
skill: mandate_enforcer
category: governance
description: Injects mandated proposals at top of sprint backlog while respecting capacity.
tier: free
inputs: current_sprint, mandated_proposals
---

# Mandate Enforcer

## Description
Injects mandated proposals at top of sprint backlog while respecting capacity.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `current_sprint` | `array` | Yes |  |
| `mandated_proposals` | `array` | Yes |  |
| `capacity_hours` | `number` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "mandate_enforcer",
  "arguments": {
    "current_sprint": [],
    "mandated_proposals": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "mandate_enforcer"`.
