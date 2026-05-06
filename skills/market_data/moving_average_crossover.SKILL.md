---
skill: moving_average_crossover
category: market_data
description: Calculates SMA/EMA crossovers and emits trading posture signals.
tier: free
inputs: prices
---

# Moving Average Crossover

## Description
Calculates SMA/EMA crossovers and emits trading posture signals.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `prices` | `array` | Yes |  |
| `short_window` | `integer` | No |  |
| `long_window` | `integer` | No |  |
| `use_ema` | `boolean` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "moving_average_crossover",
  "arguments": {
    "prices": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "moving_average_crossover"`.
