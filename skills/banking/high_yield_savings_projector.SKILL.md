---
skill: high_yield_savings_projector
category: banking
description: Project high-yield savings growth with an initial deposit and recurring monthly deposits, compounded monthly. Returns final balance and total interest earned.
tier: free
inputs: initial_deposit, monthly_deposit, apy, months
---

# High Yield Savings Projector

## Description
Project high-yield savings growth with an initial deposit and recurring monthly deposits, compounded monthly. Returns final balance and total interest earned.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `initial_deposit` | `number` | Yes | Initial deposit amount. |
| `monthly_deposit` | `number` | Yes | Recurring monthly deposit amount. |
| `apy` | `number` | Yes | Annual Percentage Yield as decimal. |
| `months` | `integer` | Yes | Number of months to project. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "high_yield_savings_projector",
  "arguments": {
    "initial_deposit": 0,
    "monthly_deposit": 0,
    "apy": 0,
    "months": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "high_yield_savings_projector"`.
