---
skill: cash_conversion_cycle_calculator
category: accounting
description: Calculates the cash conversion cycle (DIO + DSO - DPO), measuring the number of days it takes to convert inventory investments into cash.
tier: free
inputs: days_inventory, days_receivables, days_payables
---

# Cash Conversion Cycle Calculator

## Description
Calculates the cash conversion cycle (DIO + DSO - DPO), measuring the number of days it takes to convert inventory investments into cash.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `days_inventory` | `number` | Yes | Days inventory outstanding (DIO). |
| `days_receivables` | `number` | Yes | Days sales outstanding (DSO). |
| `days_payables` | `number` | Yes | Days payable outstanding (DPO). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "cash_conversion_cycle_calculator",
  "arguments": {
    "days_inventory": 0,
    "days_receivables": 0,
    "days_payables": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "cash_conversion_cycle_calculator"`.
