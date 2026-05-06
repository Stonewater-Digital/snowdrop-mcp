---
skill: rent_roll_analyzer
category: real_estate_finance
description: Calculates occupancy, income, loss-to-lease, and lease rollover risk.
tier: free
inputs: units
---

# Rent Roll Analyzer

## Description
Calculates occupancy, income, loss-to-lease, and lease rollover risk.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `units` | `array` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "rent_roll_analyzer",
  "arguments": {
    "units": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rent_roll_analyzer"`.
