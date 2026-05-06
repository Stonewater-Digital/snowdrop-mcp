---
skill: tip_calculator
category: budgeting
description: Calculates tip amount, total bill, and per-person cost with optional group split.
tier: free
inputs: bill_amount
---

# Tip Calculator

## Description
Calculates tip amount, total bill, and per-person cost with optional group split.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `bill_amount` | `number` | Yes | Total bill amount before tip in dollars. |
| `tip_percentage` | `number` | No | Tip percentage (default: 18). |
| `num_people` | `integer` | No | Number of people splitting (default: 1). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "tip_calculator",
  "arguments": {
    "bill_amount": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "tip_calculator"`.
