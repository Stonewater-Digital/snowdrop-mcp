---
skill: moving_average_crossover
category: technical_analysis
description: Compares fast and slow simple moving averages to flag golden or death cross confirmations.
tier: free
inputs: prices, fast_period, slow_period
---

# Moving Average Crossover

## Description
Compares fast and slow simple moving averages to flag golden or death cross confirmations.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `prices` | `array` | Yes | Chronological list of prices used to compute both averages. |
| `fast_period` | `integer` | Yes | Lookback for the fast moving average (e.g., 50). |
| `slow_period` | `integer` | Yes | Lookback for the slow moving average (e.g., 200). |

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
    "prices": [],
    "fast_period": 0,
    "slow_period": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "moving_average_crossover"`.
