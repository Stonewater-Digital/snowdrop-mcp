---
skill: minimum_payment_calculator
category: banking
description: Calculate credit card minimum payment, estimate months to payoff paying only the minimum, and total interest paid.
tier: free
inputs: balance, apr
---

# Minimum Payment Calculator

## Description
Calculate credit card minimum payment, estimate months to payoff paying only the minimum, and total interest paid.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `balance` | `number` | Yes | Current card balance. |
| `apr` | `number` | Yes | Annual Percentage Rate as decimal. |
| `min_pct` | `number` | No | Minimum payment as fraction of balance (default 0.02). |
| `min_floor` | `number` | No | Minimum dollar floor for payment (default 25.0). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "minimum_payment_calculator",
  "arguments": {
    "balance": 0,
    "apr": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "minimum_payment_calculator"`.
