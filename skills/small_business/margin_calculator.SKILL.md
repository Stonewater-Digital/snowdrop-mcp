---
skill: margin_calculator
category: small_business
description: Calculate profit margin percentage: (selling_price - cost) / selling_price * 100.
tier: free
inputs: cost, selling_price
---

# Margin Calculator

## Description
Calculate profit margin percentage: (selling_price - cost) / selling_price * 100.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `cost` | `number` | Yes | Product cost. |
| `selling_price` | `number` | Yes | Selling price. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "margin_calculator",
  "arguments": {
    "cost": 0,
    "selling_price": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "margin_calculator"`.
