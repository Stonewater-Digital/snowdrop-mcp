---
skill: debt_snowball_planner
category: personal_finance
description: Simulates a debt snowball strategy by ordering balances from smallest to largest, applying extra cash to the current focus account, and outputting the payoff timeline.
tier: free
inputs: debts, extra_payment
---

# Debt Snowball Planner

## Description
Simulates a debt snowball strategy by ordering balances from smallest to largest, applying extra cash to the current focus account, and outputting the payoff timeline.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `debts` | `array` | Yes | List of debts with name, balance, rate, and min_payment. |
| `extra_payment` | `number` | Yes | Additional dollars applied to the current snowball focus. |

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
