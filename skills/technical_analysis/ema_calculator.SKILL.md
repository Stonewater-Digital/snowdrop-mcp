---
skill: ema_calculator
category: technical_analysis
description: Calculates exponential moving averages using Wilder's smoothing to detect price momentum shifts.
tier: free
inputs: prices, period
---

# Ema Calculator

## Description
Calculates exponential moving averages using Wilder's smoothing to detect price momentum shifts.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `prices` | `array` | Yes | Chronological price list (oldest first). |
| `period` | `integer` | Yes | EMA lookback period (e.g., 12, 26). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "ema_calculator",
  "arguments": {
    "prices": [],
    "period": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "ema_calculator"`.
