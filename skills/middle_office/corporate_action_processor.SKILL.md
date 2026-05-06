---
skill: corporate_action_processor
category: middle_office
description: Adjusts position quantities and cash for announced corporate actions.
tier: free
inputs: position_quantity, action_type, ratio
---

# Corporate Action Processor

## Description
Adjusts position quantities and cash for announced corporate actions.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `position_quantity` | `number` | Yes |  |
| `action_type` | `string` | Yes |  |
| `ratio` | `number` | Yes |  |
| `cash_component` | `number` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "corporate_action_processor",
  "arguments": {
    "position_quantity": 0,
    "action_type": "<action_type>",
    "ratio": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "corporate_action_processor"`.
