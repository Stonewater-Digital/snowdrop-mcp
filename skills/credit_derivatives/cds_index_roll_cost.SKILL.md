---
skill: cds_index_roll_cost
category: credit_derivatives
description: Computes CDS index roll cost by comparing on/off-the-run spreads and PV01 carry over the roll period, following standard index arbitrage analytics.
tier: free
inputs: on_the_run_spread_bp, off_the_run_spread_bp, time_to_maturity_years, roll_period_years, notional, discount_rate
---

# Cds Index Roll Cost

## Description
Computes CDS index roll cost by comparing on/off-the-run spreads and PV01 carry over the roll period, following standard index arbitrage analytics.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `on_the_run_spread_bp` | `number` | Yes | Current on-the-run index spread in basis points. |
| `off_the_run_spread_bp` | `number` | Yes | Off-the-run index spread in basis points. |
| `time_to_maturity_years` | `number` | Yes | Remaining maturity for the off-the-run contract in years. |
| `roll_period_years` | `number` | Yes | Time until the next roll date in years. |
| `notional` | `number` | Yes | Index notional in currency units. |
| `discount_rate` | `number` | Yes | Continuously compounded discount rate for PV. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "cds_index_roll_cost",
  "arguments": {
    "on_the_run_spread_bp": 0,
    "off_the_run_spread_bp": 0,
    "time_to_maturity_years": 0,
    "roll_period_years": 0,
    "notional": 0,
    "discount_rate": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "cds_index_roll_cost"`.
