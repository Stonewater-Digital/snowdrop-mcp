---
skill: macro_indicator_tracker
category: market_data
description: Fetches recent FRED indicators and computes MoM trends.
tier: free
inputs: indicators
---

# Macro Indicator Tracker

## Description
Fetches recent FRED indicators and computes MoM trends.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `indicators` | `array` | Yes |  |
| `periods` | `integer` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "macro_indicator_tracker",
  "arguments": {
    "indicators": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "macro_indicator_tracker"`.
