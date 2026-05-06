---
skill: property_roi_calculator
category: real_estate
description: Calculate property return on investment from annual income, expenses, current value, and purchase price. Includes cash flow ROI and total ROI with appreciation.
tier: free
inputs: annual_income, annual_expenses, property_value, purchase_price
---

# Property Roi Calculator

## Description
Calculate property return on investment from annual income, expenses, current value, and purchase price. Includes cash flow ROI and total ROI with appreciation.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `annual_income` | `number` | Yes | Total annual income from the property in USD. |
| `annual_expenses` | `number` | Yes | Total annual expenses (taxes, insurance, maintenance, management, debt service) in USD. |
| `property_value` | `number` | Yes | Current market value of the property in USD. |
| `purchase_price` | `number` | Yes | Original purchase price in USD. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "property_roi_calculator",
  "arguments": {
    "annual_income": 0,
    "annual_expenses": 0,
    "property_value": 0,
    "purchase_price": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "property_roi_calculator"`.
