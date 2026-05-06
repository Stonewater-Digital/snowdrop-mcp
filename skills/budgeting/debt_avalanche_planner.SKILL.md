---
skill: debt_avalanche_planner
category: budgeting
description: Plans debt payoff using the avalanche method: pay minimums on all debts, apply extra payment to the highest interest rate first.
tier: free
inputs: debts, extra_payment
---

# Debt Avalanche Planner

## Description
Plans debt payoff using the avalanche method: pay minimums on all debts, apply extra payment to the highest interest rate first.

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
  "tool": "debt_avalanche_planner",
  "arguments": {
    "debts": [],
    "extra_payment": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "debt_avalanche_planner"`.
