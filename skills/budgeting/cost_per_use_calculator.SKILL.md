---
skill: cost_per_use_calculator
category: budgeting
description: Calculates cost per use for a purchase and provides value assessment.
tier: free
inputs: purchase_price, expected_uses
---

# Cost Per Use Calculator

## Description
Calculates cost per use for a purchase and provides value assessment.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `purchase_price` | `number` | Yes | The purchase price in dollars. |
| `expected_uses` | `integer` | Yes | The expected number of times the item will be used. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "cost_per_use_calculator",
  "arguments": {
    "purchase_price": 0,
    "expected_uses": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "cost_per_use_calculator"`.
