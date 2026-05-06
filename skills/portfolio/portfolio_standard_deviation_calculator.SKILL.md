---
skill: portfolio_standard_deviation_calculator
category: portfolio
description: Calculates portfolio standard deviation (volatility) from weights and a matrix of asset returns as sqrt(w^T * Cov * w).
tier: free
inputs: weights, returns_matrix
---

# Portfolio Standard Deviation Calculator

## Description
Calculates portfolio standard deviation (volatility) from weights and a matrix of asset returns as sqrt(w^T * Cov * w).

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `weights` | `array` | Yes | List of portfolio weights (should sum to 1). |
| `returns_matrix` | `array` | Yes | List of lists; each inner list is the return series for one asset. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "portfolio_standard_deviation_calculator",
  "arguments": {
    "weights": [],
    "returns_matrix": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "portfolio_standard_deviation_calculator"`.
