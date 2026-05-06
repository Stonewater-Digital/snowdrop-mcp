---
skill: state_income_tax_apportionment_model
category: securities_tax
description: Apportions taxable income among states via three-factor formula.
tier: free
inputs: states, taxable_income
---

# State Income Tax Apportionment Model

## Description
Apportions taxable income among states via three-factor formula.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `states` | `array` | Yes |  |
| `taxable_income` | `number` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "state_income_tax_apportionment_model",
  "arguments": {
    "states": [],
    "taxable_income": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "state_income_tax_apportionment_model"`.
