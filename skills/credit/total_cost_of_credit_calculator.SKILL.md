---
skill: total_cost_of_credit_calculator
category: credit
description: Calculate total cost of credit: total paid, total interest, and effective rate for a fixed-rate loan.
tier: free
inputs: principal, apr, term_months
---

# Total Cost Of Credit Calculator

## Description
Calculate total cost of credit: total paid, total interest, and effective rate for a fixed-rate loan.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `principal` | `number` | Yes | Loan principal. |
| `apr` | `number` | Yes | Annual rate as decimal. |
| `term_months` | `integer` | Yes | Loan term in months. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "total_cost_of_credit_calculator",
  "arguments": {
    "principal": 0,
    "apr": 0,
    "term_months": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "total_cost_of_credit_calculator"`.
