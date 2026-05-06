---
skill: mortgage_refinance_analyzer
category: personal_finance
description: Compares an existing mortgage to a potential refinance by modeling monthly savings, break-even period, lifetime interest, and payoff horizon.
tier: free
inputs: current_balance, current_rate, current_remaining_months, new_rate, new_term_months, closing_costs
---

# Mortgage Refinance Analyzer

## Description
Compares an existing mortgage to a potential refinance by modeling monthly savings, break-even period, lifetime interest, and payoff horizon.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `current_balance` | `number` | Yes | Outstanding principal on the existing loan. |
| `current_rate` | `number` | Yes | Current loan APR as decimal. |
| `current_remaining_months` | `number` | Yes | Months remaining on the existing mortgage. |
| `new_rate` | `number` | Yes | Proposed refinance APR as decimal. |
| `new_term_months` | `number` | Yes | Term of the new loan in months. |
| `closing_costs` | `number` | Yes | Out-of-pocket closing costs required for refinance. |

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
