---
skill: parametric_var_calculator
category: quantitative_risk
description: Basel variance-covariance VaR with component, marginal, and incremental attribution over a user horizon.
tier: free
inputs: portfolio_weights, covariance_matrix, confidence_level, horizon_days
---

# Parametric Var Calculator

## Description
Basel variance-covariance VaR with component, marginal, and incremental attribution over a user horizon.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `portfolio_weights` | `array` | Yes | Asset weights or dollar sensitivities; assumed to sum to portfolio exposure. |
| `covariance_matrix` | `array` | Yes | Square covariance matrix of asset returns expressed in decimal terms. |
| `confidence_level` | `number` | Yes | Confidence level for VaR, e.g., 0.99 for Basel 99th percentile. |
| `horizon_days` | `integer` | Yes | Liquidation horizon in trading days; VaR scales with sqrt of this horizon. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "parametric_var_calculator",
  "arguments": {
    "portfolio_weights": [],
    "covariance_matrix": [],
    "confidence_level": 0,
    "horizon_days": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "parametric_var_calculator"`.
