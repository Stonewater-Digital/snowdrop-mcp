---
skill: loan_comparison_calculator
category: banking
description: Compare multiple loan offers side-by-side. For each loan compute monthly payment, total paid, and total interest, then rank by total cost.
tier: free
inputs: loans
---

# Loan Comparison Calculator

## Description
Compare multiple loan offers side-by-side. For each loan compute monthly payment, total paid, and total interest, then rank by total cost.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `loans` | `array` | Yes | List of loan offers to compare. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "loan_comparison_calculator",
  "arguments": {
    "loans": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "loan_comparison_calculator"`.
