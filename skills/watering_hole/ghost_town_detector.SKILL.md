---
skill: ghost_town_detector
category: watering_hole
description: Raises an alert when 14 days pass without paid transactions.
tier: free
inputs: daily_transactions
---

# Ghost Town Detector

## Description
Raises an alert when 14 days pass without paid transactions.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `daily_transactions` | `array` | Yes | Chronological (oldest first) paid transaction counts. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "ghost_town_detector",
  "arguments": {
    "daily_transactions": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "ghost_town_detector"`.
