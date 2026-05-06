---
skill: portfolio_variance_calc
category: technical
description: Calculate portfolio expected return, variance, standard deviation, Sharpe ratio, and diversification benefit using Modern Portfolio Theory (MPT).
tier: free
inputs: holdings, correlation_matrix
---

# Portfolio Variance Calc

## Description
Calculate portfolio expected return, variance, standard deviation, Sharpe ratio, and diversification benefit using Modern Portfolio Theory (MPT).

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `holdings` | `array` | Yes | List of holding dicts: asset (str), weight (float, 0-1), expected_return (float, annualized decimal e.g. 0.12 for 12%), std_dev (float, annualized decimal). |
| `correlation_matrix` | `array` | Yes | NxN correlation matrix (list of lists of floats in [-1, 1]). Must match number of holdings. |
| `risk_free_rate` | `number` | No | Annualized risk-free rate (e.g. 0.05 for 5%). If provided, enables Sharpe ratio calculation. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "portfolio_variance_calc",
  "arguments": {
    "holdings": [],
    "correlation_matrix": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "portfolio_variance_calc"`.
