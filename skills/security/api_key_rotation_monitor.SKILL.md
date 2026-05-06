---
skill: api_key_rotation_monitor
category: security
description: Scores API keys by age and alerts when max_age_days is breached.
tier: free
inputs: key_inventory
---

# Api Key Rotation Monitor

## Description
Scores API keys by age and alerts when max_age_days is breached.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `key_inventory` | `array` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "api_key_rotation_monitor",
  "arguments": {
    "key_inventory": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "api_key_rotation_monitor"`.
