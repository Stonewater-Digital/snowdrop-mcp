---
skill: monte_carlo_var
category: quantitative_risk
description: Monte Carlo VaR/ES with Cholesky-based correlated shocks consistent with Basel 99% methodologies.
tier: free
inputs: expected_returns, covariance_matrix, num_simulations, horizon_days, confidence_level
---

# Monte Carlo Var

## Description
Monte Carlo VaR/ES with Cholesky-based correlated shocks consistent with Basel 99% methodologies.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `expected_returns` | `array` | Yes | Expected daily returns per asset expressed in decimals. |
| `covariance_matrix` | `array` | Yes | Positive semi-definite covariance matrix aligned with expected_returns order. |
| `num_simulations` | `integer` | Yes | Number of Monte Carlo draws for the loss distribution. |
| `horizon_days` | `integer` | Yes | Holding period for scaling simulated returns. |
| `confidence_level` | `number` | Yes | Confidence level for VaR, e.g., 0.99. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "monte_carlo_var",
  "arguments": {
    "expected_returns": [],
    "covariance_matrix": [],
    "num_simulations": 0,
    "horizon_days": 0,
    "confidence_level": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "monte_carlo_var"`.
