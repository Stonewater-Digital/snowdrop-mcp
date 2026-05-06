---
skill: burn_rate_calculator
category: small_business
description: Calculate gross burn rate (cash spent per month) and net burn rate (accounting for revenue). Gross burn = (starting_cash - ending_cash) / months.
tier: free
inputs: starting_cash, ending_cash, months
---

# Burn Rate Calculator

## Description
Calculate gross burn rate (cash spent per month) and net burn rate (accounting for revenue). Gross burn = (starting_cash - ending_cash) / months.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `starting_cash` | `number` | Yes | Cash at start of period. |
| `ending_cash` | `number` | Yes | Cash at end of period. |
| `months` | `number` | Yes | Number of months in the period. |
| `revenue` | `number` | No | Optional total revenue earned during the period. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "burn_rate_calculator",
  "arguments": {
    "starting_cash": 0,
    "ending_cash": 0,
    "months": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "burn_rate_calculator"`.
