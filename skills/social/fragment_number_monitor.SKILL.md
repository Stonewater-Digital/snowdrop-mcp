---
skill: fragment_number_monitor
category: social
description: Filters Fragment number listings by prefix and budget.
tier: free
inputs: target_prefix, max_price_ton
---

# Fragment Number Monitor

## Description
Filters Fragment number listings by prefix and budget.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `target_prefix` | `string` | Yes |  |
| `max_price_ton` | `number` | Yes |  |
| `listings` | `array` | No | Optional cached listings to scan. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "fragment_number_monitor",
  "arguments": {
    "target_prefix": "<target_prefix>",
    "max_price_ton": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "fragment_number_monitor"`.
