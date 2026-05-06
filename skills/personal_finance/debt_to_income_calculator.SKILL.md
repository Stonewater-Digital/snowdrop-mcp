---
skill: debt_to_income_calculator
category: personal_finance
description: Evaluates monthly debt obligations relative to income for mortgage qualification across Conventional, FHA, and VA programs.
tier: free
inputs: monthly_debts, gross_monthly_income
---

# Debt To Income Calculator

## Description
Evaluates monthly debt obligations relative to income for mortgage qualification across Conventional, FHA, and VA programs.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `monthly_debts` | `array` | Yes | List of debt items with type (housing/other) and amount. |
| `gross_monthly_income` | `number` | Yes | Household gross monthly income before taxes. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "debt_to_income_calculator",
  "arguments": {
    "monthly_debts": [],
    "gross_monthly_income": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "debt_to_income_calculator"`.
