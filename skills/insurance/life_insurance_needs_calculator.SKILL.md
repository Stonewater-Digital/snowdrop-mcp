---
skill: life_insurance_needs_calculator
category: insurance
description: Calculate life insurance needs: income replacement + outstanding debts + funeral costs - existing coverage.
tier: free
inputs: annual_income
---

# Life Insurance Needs Calculator

## Description
Calculate life insurance needs: income replacement + outstanding debts + funeral costs - existing coverage.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `annual_income` | `number` | Yes | Annual income to replace. |
| `years_of_income` | `integer` | No | Years of income to cover (default 10). |
| `outstanding_debts` | `number` | No | Total outstanding debts (default 0). |
| `funeral_costs` | `number` | No | Estimated funeral/burial costs (default 15000). |
| `existing_coverage` | `number` | No | Existing life insurance coverage (default 0). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "life_insurance_needs_calculator",
  "arguments": {
    "annual_income": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "life_insurance_needs_calculator"`.
