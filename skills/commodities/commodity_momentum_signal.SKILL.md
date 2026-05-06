---
skill: commodity_momentum_signal
category: commodities
description: Builds a time-series momentum signal using short and long lookback returns with volatility-adjusted scoring. Standard approach: 12-1 momentum skips the most recent month to avoid short-term reversal contamination.
tier: free
inputs: price_series
---

# Commodity Momentum Signal

## Description
Builds a time-series momentum signal using short and long lookback returns with volatility-adjusted scoring. Standard approach: 12-1 momentum skips the most recent month to avoid short-term reversal contamination.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `price_series` | `array` | Yes | Price series ordered from oldest to newest (must be > 0). At least lookback_long + 2 points. |
| `lookback_short` | `integer` | No | Short lookback window in periods for momentum computation. Default 12. |
| `lookback_long` | `integer` | No | Long lookback window for trend context. Default 36. |
| `skip_recent` | `integer` | No | Periods to skip from end (reversal avoidance). Default 1 (12-1 style). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "commodity_momentum_signal",
  "arguments": {
    "price_series": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "commodity_momentum_signal"`.
