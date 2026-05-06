---
skill: debt_snowball_planner
category: budgeting
description: Plans debt payoff using the snowball method: pay minimums on all debts, apply extra payment to the smallest balance first.
tier: free
inputs: debts, extra_payment
---

# Debt Snowball Planner

## Description
Plans debt payoff using the snowball method: pay minimums on all debts, apply extra payment to the smallest balance first.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `debts` | `array` | Yes | List of debts with name, balance, minimum payment, and interest rate. |
| `extra_payment` | `number` | Yes | Additional monthly amount to apply toward debt payoff. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "debt_snowball_planner",
  "arguments": {
    "debts": [],
    "extra_payment": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "debt_snowball_planner"`.
