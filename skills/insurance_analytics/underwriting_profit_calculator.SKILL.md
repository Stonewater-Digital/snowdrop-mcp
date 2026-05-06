---
skill: underwriting_profit_calculator
category: insurance_analytics
description: Computes underwriting profit/loss, underwriting margin, combined ratio, and return on net earned premium from earned premium, losses, and expenses.
tier: free
inputs: earned_premium, incurred_losses, underwriting_expenses
---

# Underwriting Profit Calculator

## Description
Computes underwriting profit/loss, underwriting margin, combined ratio, and return on net earned premium from earned premium, losses, and expenses.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `earned_premium` | `number` | Yes | Net earned premium for the period. Must be > 0. |
| `incurred_losses` | `number` | Yes | Incurred losses including IBNR (paid + reserves). Must be >= 0. |
| `underwriting_expenses` | `number` | Yes | Total underwriting expenses (acquisition + G&A + taxes/fees). Must be >= 0. |
| `policyholder_dividends` | `number` | No | Policyholder dividends paid or accrued. Must be >= 0. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "underwriting_profit_calculator",
  "arguments": {
    "earned_premium": 0,
    "incurred_losses": 0,
    "underwriting_expenses": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "underwriting_profit_calculator"`.
