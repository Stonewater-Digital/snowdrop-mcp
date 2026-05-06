---
skill: williams_percent_r
category: technical_analysis
description: Calculates Larry Williams' %R oscillator comparing close versus the highest/lowest range.
tier: free
inputs: highs, lows, closes, period
---

# Williams Percent R

## Description
Calculates Larry Williams' %R oscillator comparing close versus the highest/lowest range.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `highs` | `array` | Yes | High prices. |
| `lows` | `array` | Yes | Low prices. |
| `closes` | `array` | Yes | Close prices. |
| `period` | `integer` | Yes | Lookback length for %R (default 14). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "williams_percent_r",
  "arguments": {
    "highs": [],
    "lows": [],
    "closes": [],
    "period": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "williams_percent_r"`.
