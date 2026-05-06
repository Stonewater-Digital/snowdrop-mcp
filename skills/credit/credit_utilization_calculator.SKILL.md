---
skill: credit_utilization_calculator
category: credit
description: Calculate credit utilization ratio per card and overall. Provides total balance, total limit, and utilization percentages.
tier: free
inputs: balances, limits
---

# Credit Utilization Calculator

## Description
Calculate credit utilization ratio per card and overall. Provides total balance, total limit, and utilization percentages.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `balances` | `array` | Yes | List of current balances for each card. |
| `limits` | `array` | Yes | List of credit limits for each card (same order as balances). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "credit_utilization_calculator",
  "arguments": {
    "balances": [],
    "limits": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "credit_utilization_calculator"`.
