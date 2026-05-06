---
skill: surety_bond_capacity_calculator
category: corporate_insurance
description: Estimates surety bonding capacity from financial statements.
tier: free
inputs: working_capital, net_worth, backlog
---

# Surety Bond Capacity Calculator

## Description
Estimates surety bonding capacity from financial statements.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `working_capital` | `number` | Yes |  |
| `net_worth` | `number` | Yes |  |
| `backlog` | `number` | Yes |  |
| `bonding_multiplier` | `number` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "surety_bond_capacity_calculator",
  "arguments": {
    "working_capital": 0,
    "net_worth": 0,
    "backlog": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "surety_bond_capacity_calculator"`.
