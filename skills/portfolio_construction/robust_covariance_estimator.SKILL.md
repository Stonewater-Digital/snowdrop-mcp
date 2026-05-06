---
skill: robust_covariance_estimator
category: portfolio_construction
description: Produces Ledoit-Wolf shrunk covariance and a Minimum Covariance Determinant (MCD) estimate to stabilize mean-variance inputs against outliers and regime shifts.
tier: free
inputs: return_series
---

# Robust Covariance Estimator

## Description
Produces Ledoit-Wolf shrunk covariance and a Minimum Covariance Determinant (MCD) estimate to stabilize mean-variance inputs against outliers and regime shifts.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `return_series` | `array` | Yes | Matrix of historical returns (rows=observations, columns=assets). |
| `subset_fraction` | `number` | No | Fraction of observations used for the MCD subset (default 0.75). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "robust_covariance_estimator",
  "arguments": {
    "return_series": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "robust_covariance_estimator"`.
