---
skill: cash_conversion_cycle
category: financial_analysis
description: Computes DSO, DIO, DPO, and the cash conversion cycle to assess working capital efficiency.
tier: free
inputs: revenue, cogs, receivables, inventory, payables, prior_receivables, prior_inventory, prior_payables
---

# Cash Conversion Cycle

## Description
Computes DSO, DIO, DPO, and the cash conversion cycle to assess working capital efficiency.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `revenue` | `number` | Yes |  |
| `cogs` | `number` | Yes |  |
| `receivables` | `number` | Yes |  |
| `inventory` | `number` | Yes |  |
| `payables` | `number` | Yes |  |
| `prior_receivables` | `number` | Yes |  |
| `prior_inventory` | `number` | Yes |  |
| `prior_payables` | `number` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "cash_conversion_cycle",
  "arguments": {
    "revenue": 0,
    "cogs": 0,
    "receivables": 0,
    "inventory": 0,
    "payables": 0,
    "prior_receivables": 0,
    "prior_inventory": 0,
    "prior_payables": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "cash_conversion_cycle"`.
