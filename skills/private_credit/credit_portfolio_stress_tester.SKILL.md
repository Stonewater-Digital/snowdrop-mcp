---
skill: credit_portfolio_stress_tester
category: private_credit
description: Applies EBITDA declines and rate shocks to measure coverage and leverage impact.
tier: free
inputs: base_ebitda, base_interest_expense, total_debt
---

# Credit Portfolio Stress Tester

## Description
Applies EBITDA declines and rate shocks to measure coverage and leverage impact.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `base_ebitda` | `number` | Yes |  |
| `base_interest_expense` | `number` | Yes |  |
| `total_debt` | `number` | Yes |  |
| `rate_shock_bps` | `number` | No |  |
| `ebitda_decline_pct` | `number` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "credit_portfolio_stress_tester",
  "arguments": {
    "base_ebitda": 0,
    "base_interest_expense": 0,
    "total_debt": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "credit_portfolio_stress_tester"`.
