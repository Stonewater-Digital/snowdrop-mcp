---
skill: loan_to_value_calculator
category: private_credit
description: Calculates senior and total LTV ratios with headroom checks.
tier: free
inputs: collateral_value, senior_debt, total_debt
---

# Loan To Value Calculator

## Description
Calculates senior and total LTV ratios with headroom checks.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `collateral_value` | `number` | Yes |  |
| `senior_debt` | `number` | Yes |  |
| `total_debt` | `number` | Yes |  |
| `advance_rate_limit` | `number` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "loan_to_value_calculator",
  "arguments": {
    "collateral_value": 0,
    "senior_debt": 0,
    "total_debt": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "loan_to_value_calculator"`.
