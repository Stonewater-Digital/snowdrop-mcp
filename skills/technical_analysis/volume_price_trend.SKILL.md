---
skill: volume_price_trend
category: technical_analysis
description: Calculates cumulative Volume Price Trend and compares against SMA to detect divergences.
tier: free
inputs: closes, volumes, sma_period
---

# Volume Price Trend

## Description
Calculates cumulative Volume Price Trend and compares against SMA to detect divergences.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `closes` | `array` | Yes | Close prices. |
| `volumes` | `array` | Yes | Volumes aligned with closes. |
| `sma_period` | `integer` | Yes | SMA period for VPT smoothing. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "volume_price_trend",
  "arguments": {
    "closes": [],
    "volumes": [],
    "sma_period": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "volume_price_trend"`.
