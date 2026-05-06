---
skill: markup_calculator
category: small_business
description: Calculate markup percentage: (selling_price - cost) / cost * 100.
tier: free
inputs: cost, selling_price
---

# Markup Calculator

## Description
Calculate markup percentage: (selling_price - cost) / cost * 100.

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
  "tool": "markup_calculator",
  "arguments": {
    "cost": 0,
    "selling_price": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "markup_calculator"`.
