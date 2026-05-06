---
skill: risk_budgeting_allocator
category: portfolio_construction
description: Computes equal-risk-contribution weights (a la Maillard, Roncalli, Teiletche 2010) by solving for the portfolio weights whose marginal contributions match risk budgets.
tier: free
inputs: covariance_matrix
---

# Risk Budgeting Allocator

## Description
Computes equal-risk-contribution weights (a la Maillard, Roncalli, Teiletche 2010) by solving for the portfolio weights whose marginal contributions match risk budgets.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `covariance_matrix` | `array` | Yes | Covariance matrix of asset returns. |
| `risk_budgets` | `array` | No | Target share of total risk contributed by each asset (sums to 1). |
| `tolerance` | `number` | No | Stopping tolerance for Euler equation residuals (default 1e-6). |
| `max_iterations` | `integer` | No | Maximum Newton steps (default 200). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "risk_budgeting_allocator",
  "arguments": {
    "covariance_matrix": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "risk_budgeting_allocator"`.
