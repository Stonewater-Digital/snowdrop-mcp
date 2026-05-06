---
skill: portfolio_variance_calculator
category: market_analytics
description: Computes covariance matrix, portfolio variance/volatility, and risk contributions from asset weights.
tier: free
inputs: weights, returns_matrix
---

# Portfolio Variance Calculator

## Description
Computes covariance matrix, portfolio variance/volatility, and risk contributions from asset weights.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `weights` | `array` | Yes | Portfolio weights (sum to 1). |
| `returns_matrix` | `array` | Yes | List of return series for each asset. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "portfolio_variance_calculator",
  "arguments": {
    "weights": [],
    "returns_matrix": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "portfolio_variance_calculator"`.
