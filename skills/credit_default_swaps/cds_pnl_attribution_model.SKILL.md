---
skill: cds_pnl_attribution_model
category: credit_default_swaps
description: Attributes CDS P&L into carry, spread, and curve components.
tier: free
inputs: notional, spread_change_bps, pv01, carry_income, curve_roll
---

# Cds Pnl Attribution Model

## Description
Attributes CDS P&L into carry, spread, and curve components.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `notional` | `number` | Yes |  |
| `spread_change_bps` | `number` | Yes |  |
| `pv01` | `number` | Yes |  |
| `carry_income` | `number` | Yes |  |
| `curve_roll` | `number` | Yes |  |
| `fx_impact` | `number` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "cds_pnl_attribution_model",
  "arguments": {
    "notional": 0,
    "spread_change_bps": 0,
    "pv01": 0,
    "carry_income": 0,
    "curve_roll": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "cds_pnl_attribution_model"`.
