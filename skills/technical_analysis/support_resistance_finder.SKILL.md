---
skill: support_resistance_finder
category: technical_analysis
description: Finds price levels with multiple touches using swing highs/lows within a lookback window.
tier: free
inputs: highs, lows, closes, lookback, num_touches_required
---

# Support Resistance Finder

## Description
Finds price levels with multiple touches using swing highs/lows within a lookback window.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `highs` | `array` | Yes | High prices (oldest first). |
| `lows` | `array` | Yes | Low prices. |
| `closes` | `array` | Yes | Close prices. |
| `lookback` | `integer` | Yes | Bars to inspect on each side for pivots. |
| `num_touches_required` | `integer` | Yes | Minimum touches to validate a level. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "support_resistance_finder",
  "arguments": {
    "highs": [],
    "lows": [],
    "closes": [],
    "lookback": 0,
    "num_touches_required": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "support_resistance_finder"`.
