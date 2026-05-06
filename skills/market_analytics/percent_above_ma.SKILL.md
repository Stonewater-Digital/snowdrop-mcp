---
skill: percent_above_ma
category: market_analytics
description: Calculates % of symbols above their moving average to gauge breadth thrusts.
tier: free
inputs: stock_closes_matrix, ma_period
---

# Percent Above Ma

## Description
Calculates % of symbols above their moving average to gauge breadth thrusts.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `stock_closes_matrix` | `array` | Yes | List of closing-price series per stock. |
| `ma_period` | `integer` | Yes | Moving-average lookback (e.g., 200). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "percent_above_ma",
  "arguments": {
    "stock_closes_matrix": [],
    "ma_period": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "percent_above_ma"`.
