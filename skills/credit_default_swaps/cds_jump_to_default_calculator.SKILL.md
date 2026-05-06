---
skill: cds_jump_to_default_calculator
category: credit_default_swaps
description: Calculates jump-to-default impact using LGD and recovery assumptions.
tier: free
inputs: notional, recovery_rate_pct, current_spread_bps
---

# Cds Jump To Default Calculator

## Description
Calculates jump-to-default impact using LGD and recovery assumptions.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `notional` | `number` | Yes |  |
| `recovery_rate_pct` | `number` | Yes |  |
| `current_spread_bps` | `number` | Yes |  |
| `accrued_coupon_bps` | `number` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "cds_jump_to_default_calculator",
  "arguments": {
    "notional": 0,
    "recovery_rate_pct": 0,
    "current_spread_bps": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "cds_jump_to_default_calculator"`.
