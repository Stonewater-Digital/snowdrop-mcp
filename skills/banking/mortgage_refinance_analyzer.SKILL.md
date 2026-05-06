---
skill: mortgage_refinance_analyzer
category: banking
description: Analyze whether refinancing a mortgage is worthwhile. Compare current vs new monthly payments, calculate breakeven month for closing costs, and total savings over the loan.
tier: free
inputs: current_balance, current_rate, current_remaining_months, new_rate, new_term_months, closing_costs
---

# Mortgage Refinance Analyzer

## Description
Analyze whether refinancing a mortgage is worthwhile. Compare current vs new monthly payments, calculate breakeven month for closing costs, and total savings over the loan.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `current_balance` | `number` | Yes | Remaining loan balance. |
| `current_rate` | `number` | Yes | Current annual rate as decimal. |
| `current_remaining_months` | `integer` | Yes | Months remaining on current loan. |
| `new_rate` | `number` | Yes | New annual rate as decimal. |
| `new_term_months` | `integer` | Yes | Term of the new loan in months. |
| `closing_costs` | `number` | Yes | Total closing costs for refinance. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "mortgage_refinance_analyzer",
  "arguments": {
    "current_balance": 0,
    "current_rate": 0,
    "current_remaining_months": 0,
    "new_rate": 0,
    "new_term_months": 0,
    "closing_costs": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "mortgage_refinance_analyzer"`.
