---
skill: commitment_pacing_model
category: fund_accounting
description: Suggests annual commitments and overcommitment ratios for PE allocation targets. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: total_portfolio, target_pe_allocation_pct, current_pe_nav, unfunded_commitments, expected_distributions_annual, expected_calls_annual, new_fund_avg_size
---

# Commitment Pacing Model

## Description
Suggests annual commitments and overcommitment ratios for PE allocation targets. (Premium — subscribe at https://snowdrop.ai)

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `total_portfolio` | `number` | Yes | Total portfolio value in dollars (all asset classes). |
| `target_pe_allocation_pct` | `number` | Yes | Target PE allocation as a decimal (e.g. `0.20` for 20%). |
| `current_pe_nav` | `number` | Yes | Current NAV of existing PE holdings in dollars. |
| `unfunded_commitments` | `number` | Yes | Total uncalled capital commitments already made in dollars. |
| `expected_distributions_annual` | `number` | Yes | Expected annual PE distributions (return of capital + proceeds) in dollars. |
| `expected_calls_annual` | `number` | Yes | Expected capital calls to be drawn in the next 12 months in dollars. |
| `new_fund_avg_size` | `number` | Yes | Average commitment size for new fund subscriptions in dollars. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "commitment_pacing_model",
  "arguments": {
    "total_portfolio": 500000000,
    "target_pe_allocation_pct": 0.20,
    "current_pe_nav": 75000000,
    "unfunded_commitments": 30000000,
    "expected_distributions_annual": 12000000,
    "expected_calls_annual": 15000000,
    "new_fund_avg_size": 10000000
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "commitment_pacing_model"`.
