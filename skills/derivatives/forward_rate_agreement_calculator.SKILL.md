---
skill: forward_rate_agreement_calculator
category: derivatives
description: Calculates FRA settlement amounts given contracted and market rates.
tier: free
inputs: notional, fra_rate_pct, settlement_rate_pct, contract_period_days
---

# Forward Rate Agreement Calculator

## Description
Calculates FRA settlement amounts given contracted and market rates.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `notional` | `number` | Yes | FRA notional amount. Must be > 0. |
| `fra_rate_pct` | `number` | Yes | Contracted FRA rate as a percentage. |
| `settlement_rate_pct` | `number` | Yes | LIBOR/SOFR fixing rate at settlement, as a percentage. |
| `contract_period_days` | `integer` | Yes | Length of the FRA contract period in days. |
| `settlement_delay_days` | `integer` | No | Settlement lag in days (default 2 for T+2). |
| `day_count_convention` | `string` | No | Day count convention for accrual fraction. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "forward_rate_agreement_calculator",
  "arguments": {
    "notional": 0,
    "fra_rate_pct": 0,
    "settlement_rate_pct": 0,
    "contract_period_days": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "forward_rate_agreement_calculator"`.
