---
skill: pnl_attribution_calculator
category: middle_office
description: Breaks daily P&L into price, carry, FX, and fee components.
tier: free
inputs: price_pnl, carry_pnl, fx_pnl, fee_pnl
---

# Pnl Attribution Calculator

## Description
Breaks daily P&L into price, carry, FX, and fee components.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `price_pnl` | `number` | Yes |  |
| `carry_pnl` | `number` | Yes |  |
| `fx_pnl` | `number` | Yes |  |
| `fee_pnl` | `number` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "pnl_attribution_calculator",
  "arguments": {
    "price_pnl": 0,
    "carry_pnl": 0,
    "fx_pnl": 0,
    "fee_pnl": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "pnl_attribution_calculator"`.
