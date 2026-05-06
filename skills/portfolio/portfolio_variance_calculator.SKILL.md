---
skill: portfolio_variance_calculator
category: portfolio
description: Calculates portfolio variance using weights and a matrix of asset returns. Computes w^T * Cov * w using the sample covariance matrix.
tier: free
inputs: weights, returns_matrix
---

# Portfolio Variance Calculator

## Description
Calculates portfolio variance using weights and a matrix of asset returns. Computes w^T * Cov * w using the sample covariance matrix.

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
  "tool": "portfolio_variance_calculator",
  "arguments": {
    "weights": [],
    "returns_matrix": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "portfolio_variance_calculator"`.
