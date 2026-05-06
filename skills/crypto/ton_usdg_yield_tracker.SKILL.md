---
skill: ton_usdg_yield_tracker
category: crypto
description: Calculates accrued USDG yield for TON staking ladders.
tier: free
inputs: principal, apy_pct, days_staked
---

# Ton Usdg Yield Tracker

## Description
Calculates accrued USDG yield for TON staking ladders.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `principal` | `number` | Yes |  |
| `apy_pct` | `number` | Yes |  |
| `days_staked` | `integer` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "ton_usdg_yield_tracker",
  "arguments": {
    "principal": 0,
    "apy_pct": 0,
    "days_staked": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "ton_usdg_yield_tracker"`.
