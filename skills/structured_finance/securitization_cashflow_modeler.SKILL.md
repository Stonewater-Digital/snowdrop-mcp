---
skill: securitization_cashflow_modeler
category: structured_finance
description: Generates month-by-month cash flow projections including CPR/CDR and servicing fees.
tier: free
inputs: pool_balance, wac, wam, cpr, cdr, recovery_rate, servicing_fee_pct
---

# Securitization Cashflow Modeler

## Description
Generates month-by-month cash flow projections including CPR/CDR and servicing fees.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `pool_balance` | `number` | Yes |  |
| `wac` | `number` | Yes |  |
| `wam` | `integer` | Yes |  |
| `cpr` | `number` | Yes |  |
| `cdr` | `number` | Yes |  |
| `recovery_rate` | `number` | Yes |  |
| `servicing_fee_pct` | `number` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "securitization_cashflow_modeler",
  "arguments": {
    "pool_balance": 0,
    "wac": 0,
    "wam": 0,
    "cpr": 0,
    "cdr": 0,
    "recovery_rate": 0,
    "servicing_fee_pct": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "securitization_cashflow_modeler"`.
