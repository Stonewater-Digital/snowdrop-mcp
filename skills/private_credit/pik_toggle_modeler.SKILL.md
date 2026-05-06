---
skill: pik_toggle_modeler
category: private_credit
description: Builds period schedules for cash and PIK interest accruals.
tier: free
inputs: principal, cash_coupon_pct, pik_coupon_pct, toggle_type, pik_periods, total_periods
---

# Pik Toggle Modeler

## Description
Builds period schedules for cash and PIK interest accruals.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `principal` | `number` | Yes |  |
| `cash_coupon_pct` | `number` | Yes |  |
| `pik_coupon_pct` | `number` | Yes |  |
| `toggle_type` | `string` | Yes |  |
| `pik_periods` | `integer` | Yes |  |
| `total_periods` | `integer` | Yes |  |
| `compounding` | `string` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "pik_toggle_modeler",
  "arguments": {
    "principal": 0,
    "cash_coupon_pct": 0,
    "pik_coupon_pct": 0,
    "toggle_type": "<toggle_type>",
    "pik_periods": 0,
    "total_periods": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "pik_toggle_modeler"`.
