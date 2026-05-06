---
skill: rate_card_manager
category: pricing
description: Retrieves or updates tier pricing for Watering Hole skills.
tier: free
inputs: operation, tier
---

# Rate Card Manager

## Description
Retrieves or updates tier pricing for Watering Hole skills.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `operation` | `string` | Yes |  |
| `tier` | `string` | Yes |  |
| `skill_name` | `string` | No |  |
| `price_per_call` | `number` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "rate_card_manager",
  "arguments": {
    "operation": "<operation>",
    "tier": "<tier>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rate_card_manager"`.
