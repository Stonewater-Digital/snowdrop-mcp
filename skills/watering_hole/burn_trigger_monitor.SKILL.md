---
skill: burn_trigger_monitor
category: watering_hole
description: Flags Watering Hole burn when expenses beat revenue+labor by 20% for 3 weeks.
tier: free
inputs: weekly_financials
---

# Burn Trigger Monitor

## Description
Flags Watering Hole burn when expenses beat revenue+labor by 20% for 3 weeks.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `weekly_financials` | `array` | Yes | Chronological weekly ledger entries (newest last). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "burn_trigger_monitor",
  "arguments": {
    "weekly_financials": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "burn_trigger_monitor"`.
