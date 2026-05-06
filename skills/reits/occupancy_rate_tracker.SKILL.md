---
skill: occupancy_rate_tracker
category: reits
description: Computes weighted average occupancy and vacancy by property type.
tier: free
inputs: properties
---

# Occupancy Rate Tracker

## Description
Computes weighted average occupancy and vacancy by property type.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `properties` | `array` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "occupancy_rate_tracker",
  "arguments": {
    "properties": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "occupancy_rate_tracker"`.
