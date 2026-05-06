---
skill: mass_index
category: technical_analysis
description: Implements Donald Dorsey's Mass Index using double EMA of high-low range.
tier: free
inputs: highs, lows, ema_period, sum_period
---

# Mass Index

## Description
Implements Donald Dorsey's Mass Index using double EMA of high-low range.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `highs` | `array` | Yes | High price series. |
| `lows` | `array` | Yes | Low price series. |
| `ema_period` | `integer` | Yes | EMA period (default 9). |
| `sum_period` | `integer` | Yes | Summation period for bulge detection (default 25). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "mass_index",
  "arguments": {
    "highs": [],
    "lows": [],
    "ema_period": 0,
    "sum_period": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "mass_index"`.
