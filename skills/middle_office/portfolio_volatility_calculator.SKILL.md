---
skill: portfolio_volatility_calculator
category: middle_office
description: Estimates portfolio variance and volatility from a covariance matrix.
tier: free
inputs: weights, covariance_matrix
---

# Portfolio Volatility Calculator

## Description
Estimates portfolio variance and volatility from a covariance matrix.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `weights` | `array` | Yes |  |
| `covariance_matrix` | `array` | Yes |  |
| `period_label` | `string` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "portfolio_volatility_calculator",
  "arguments": {
    "weights": [],
    "covariance_matrix": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "portfolio_volatility_calculator"`.
