---
skill: debt_avalanche_planner
category: personal_finance
description: Simulates the debt avalanche payoff strategy (highest interest rate first) and contrasts it against a classic snowball to highlight savings.
tier: free
inputs: debts, extra_payment
---

# Debt Avalanche Planner

## Description
Simulates the debt avalanche payoff strategy (highest interest rate first) and contrasts it against a classic snowball to highlight savings.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `debts` | `array` | Yes | List of debts with name, balance, rate, and min_payment. |
| `extra_payment` | `number` | Yes | Additional monthly dollars directed at the focus debt. |

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
