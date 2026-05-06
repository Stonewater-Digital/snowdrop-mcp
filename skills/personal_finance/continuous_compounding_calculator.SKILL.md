---
skill: continuous_compounding_calculator
category: personal_finance
description: Applies Pe^rt to compute the continuously compounded future value and compares it to annual and monthly compounding scenarios.
tier: free
inputs: principal, annual_rate, years
---

# Continuous Compounding Calculator

## Description
Applies Pe^rt to compute the continuously compounded future value and compares it to annual and monthly compounding scenarios.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `principal` | `number` | Yes | Initial dollars invested, must be positive. |
| `annual_rate` | `number` | Yes | Annual growth rate as decimal. |
| `years` | `number` | Yes | Holding period in years. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "continuous_compounding_calculator",
  "arguments": {
    "principal": 0,
    "annual_rate": 0,
    "years": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "continuous_compounding_calculator"`.
