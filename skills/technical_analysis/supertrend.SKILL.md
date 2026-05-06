---
skill: supertrend
category: technical_analysis
description: Applies the Supertrend algorithm (ATR bands with dynamic flips) to mark trailing stops and trend phase.
tier: free
inputs: highs, lows, closes, period, multiplier
---

# Supertrend

## Description
Applies the Supertrend algorithm (ATR bands with dynamic flips) to mark trailing stops and trend phase.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `highs` | `array` | Yes | High price series. |
| `lows` | `array` | Yes | Low price series. |
| `closes` | `array` | Yes | Close price series. |
| `period` | `integer` | Yes | ATR lookback (default 10). |
| `multiplier` | `number` | Yes | ATR multiplier (default 3). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "supertrend",
  "arguments": {
    "highs": [],
    "lows": [],
    "closes": [],
    "period": 0,
    "multiplier": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "supertrend"`.
