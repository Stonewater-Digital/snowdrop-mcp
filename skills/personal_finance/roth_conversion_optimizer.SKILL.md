---
skill: roth_conversion_optimizer
category: personal_finance
description: Quantifies the up-front tax bill, future tax savings, and breakeven timing for a Roth conversion using bracket differentials and an assumed 5% growth rate.
tier: free
inputs: traditional_ira_balance, current_tax_bracket, expected_retirement_bracket, conversion_amount, years_to_retirement
---

# Roth Conversion Optimizer

## Description
Quantifies the up-front tax bill, future tax savings, and breakeven timing for a Roth conversion using bracket differentials and an assumed 5% growth rate.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `traditional_ira_balance` | `number` | Yes | Total balance in pre-tax IRA dollars. |
| `current_tax_bracket` | `number` | Yes | Marginal federal tax rate today as decimal (e.g., 0.22). |
| `expected_retirement_bracket` | `number` | Yes | Anticipated marginal rate in retirement as decimal. |
| `conversion_amount` | `number` | Yes | Dollar amount you plan to convert to Roth now. |
| `years_to_retirement` | `number` | Yes | Years until retirement when withdrawals begin. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "roth_conversion_optimizer",
  "arguments": {
    "traditional_ira_balance": 0,
    "current_tax_bracket": 0,
    "expected_retirement_bracket": 0,
    "conversion_amount": 0,
    "years_to_retirement": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "roth_conversion_optimizer"`.
