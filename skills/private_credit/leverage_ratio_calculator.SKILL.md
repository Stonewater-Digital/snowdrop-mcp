---
skill: leverage_ratio_calculator
category: private_credit
description: Calculates gross, net, and senior leverage metrics versus targets.
tier: free
inputs: total_debt, senior_debt, cash_balance, ebitda
---

# Leverage Ratio Calculator

## Description
Calculates gross, net, and senior leverage metrics versus targets.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `total_debt` | `number` | Yes |  |
| `senior_debt` | `number` | Yes |  |
| `cash_balance` | `number` | Yes |  |
| `ebitda` | `number` | Yes |  |
| `target_total_leverage` | `number` | No |  |
| `target_senior_leverage` | `number` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "leverage_ratio_calculator",
  "arguments": {
    "total_debt": 0,
    "senior_debt": 0,
    "cash_balance": 0,
    "ebitda": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "leverage_ratio_calculator"`.
