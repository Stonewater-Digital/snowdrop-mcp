---
skill: sinking_fund_calculator
category: budgeting
description: Calculates the monthly contribution needed to save a target amount by a deadline.
tier: free
inputs: target_amount, months_until_needed
---

# Sinking Fund Calculator

## Description
Calculates the monthly contribution needed to save a target amount by a deadline.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `target_amount` | `number` | Yes | The total amount you need to save in dollars. |
| `months_until_needed` | `number` | Yes | Number of months until the money is needed. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "sinking_fund_calculator",
  "arguments": {
    "target_amount": 0,
    "months_until_needed": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "sinking_fund_calculator"`.
