---
skill: mean_reversion_score
category: market_analytics
description: Computes z-score of price versus rolling mean and estimates Ornstein-Uhlenbeck half-life.
tier: free
inputs: prices, lookback, z_threshold
---

# Mean Reversion Score

## Description
Computes z-score of price versus rolling mean and estimates Ornstein-Uhlenbeck half-life.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `prices` | `array` | Yes | Price series. |
| `lookback` | `integer` | Yes | Lookback window for mean/std. |
| `z_threshold` | `number` | Yes | Z-score trigger for signals. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "mean_reversion_score",
  "arguments": {
    "prices": [],
    "lookback": 0,
    "z_threshold": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "mean_reversion_score"`.
