---
skill: merit_review_state_identifier
category: securities_tax
description: Identifies merit review states for state securities registration planning.
tier: free
inputs: states
---

# Merit Review State Identifier

## Description
Identifies merit review states for state securities registration planning.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `states` | `array` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "merit_review_state_identifier",
  "arguments": {
    "states": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "merit_review_state_identifier"`.
