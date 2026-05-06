---
skill: volatility_rank_percentile
category: market_analytics
description: Calculates IV rank and percentile to understand volatility regimes.
tier: free
inputs: current_iv, historical_iv_series
---

# Volatility Rank Percentile

## Description
Calculates IV rank and percentile to understand volatility regimes.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `current_iv` | `number` | Yes | Current implied volatility (decimal). |
| `historical_iv_series` | `array` | Yes | History of implied vol values (>=252 observations). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "volatility_rank_percentile",
  "arguments": {
    "current_iv": 0,
    "historical_iv_series": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "volatility_rank_percentile"`.
