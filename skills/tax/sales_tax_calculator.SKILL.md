---
skill: sales_tax_calculator
category: tax
description: Calculate total sales tax from state and local rates. Returns tax amount, total cost, and combined rate.
tier: free
inputs: purchase_amount, state_rate
---

# Sales Tax Calculator

## Description
Calculate total sales tax from state and local rates. Returns tax amount, total cost, and combined rate.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `purchase_amount` | `number` | Yes | Purchase amount before tax in USD. |
| `state_rate` | `number` | Yes | State sales tax rate as a decimal (e.g. 0.06 for 6%). |
| `local_rate` | `number` | No | Local (city/county) sales tax rate as a decimal. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "sales_tax_calculator",
  "arguments": {
    "purchase_amount": 0,
    "state_rate": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "sales_tax_calculator"`.
