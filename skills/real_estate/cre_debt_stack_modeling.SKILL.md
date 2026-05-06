---
skill: cre_debt_stack_modeling
category: real_estate
description: Models a commercial real estate capital stack with senior debt, mezzanine, and equity tranches. Calculates blended cost of capital, cumulative LTV per tranche, and flags structural risk (e.g., LTV > 80% for senior).
tier: free
inputs: total_value, loan_tranches
---

# Cre Debt Stack Modeling

## Description
Models a commercial real estate capital stack with senior debt, mezzanine, and equity tranches. Calculates blended cost of capital, cumulative LTV per tranche, and flags structural risk (e.g., LTV > 80% for senior).

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `total_value` | `number` | Yes | Appraised or purchase price of the property (dollars). |
| `loan_tranches` | `array` | Yes | List of debt/equity tranches ordered by waterfall priority. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "cre_debt_stack_modeling",
  "arguments": {
    "total_value": 0,
    "loan_tranches": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "cre_debt_stack_modeling"`.
