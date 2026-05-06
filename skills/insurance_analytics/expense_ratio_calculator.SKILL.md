---
skill: expense_ratio_calculator
category: insurance_analytics
description: Computes underwriting expense ratio and breakdowns for acquisition, general & administrative, and other expenses. Supports both trade basis (vs.
tier: free
inputs: acquisition_expenses, general_admin_expenses, net_written_premium
---

# Expense Ratio Calculator

## Description
Computes underwriting expense ratio and breakdowns for acquisition, general & administrative, and other expenses. Supports both trade basis (vs. NWP) and statutory basis (vs. NEP).

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `acquisition_expenses` | `number` | Yes | Agent commissions, brokerage fees, and other policy acquisition costs. Must be >= 0. |
| `general_admin_expenses` | `number` | Yes | General and administrative overhead expenses. Must be >= 0. |
| `net_written_premium` | `number` | Yes | Net written premium (denominator for trade basis). Must be > 0. |
| `other_expenses` | `number` | No | Other underwriting expenses not captured above (taxes, licenses, fees). Must be >= 0. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "expense_ratio_calculator",
  "arguments": {
    "acquisition_expenses": 0,
    "general_admin_expenses": 0,
    "net_written_premium": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "expense_ratio_calculator"`.
