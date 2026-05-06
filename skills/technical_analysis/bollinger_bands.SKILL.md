---
skill: bollinger_bands
category: technical_analysis
description: Calculates SMA-based Bollinger Bands with configurable standard deviation multipliers.
tier: free
inputs: prices, period, num_std
---

# Bollinger Bands

## Description
Calculates SMA-based Bollinger Bands with configurable standard deviation multipliers.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `prices` | `array` | Yes | Price list (oldest first). |
| `period` | `integer` | Yes | SMA lookback (default 20). |
| `num_std` | `number` | Yes | Standard deviation multiplier (default 2). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "bollinger_bands",
  "arguments": {
    "prices": [],
    "period": 0,
    "num_std": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "bollinger_bands"`.
