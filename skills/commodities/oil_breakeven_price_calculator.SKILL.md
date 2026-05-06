---
skill: oil_breakeven_price_calculator
category: commodities
description: Determines the breakeven oil price for an upstream producer including lifting costs, opex, sustaining capex, royalties, production taxes, and a target return margin. Supports both simple and government-take deduction methods.
tier: free
inputs: lifting_cost_per_bbl, opex_per_bbl
---

# Oil Breakeven Price Calculator

## Description
Determines the breakeven oil price for an upstream producer including lifting costs, opex, sustaining capex, royalties, production taxes, and a target return margin. Supports both simple and government-take deduction methods.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `lifting_cost_per_bbl` | `number` | Yes | Direct lifting/extraction cost per barrel (must be >= 0). |
| `opex_per_bbl` | `number` | Yes | Operating expenditure per barrel excluding lifting (must be >= 0). |
| `sustaining_capex_per_bbl` | `number` | No | Sustaining capital expenditure per barrel (must be >= 0). |
| `royalty_pct` | `number` | No | Royalty rate as % of gross revenue (0–100). Defaults to 5%. |
| `tax_pct` | `number` | No | Production tax / corporate tax rate as % of net revenue (0–100). Defaults to 20%. |
| `target_margin_pct` | `number` | No | Required return margin as % of breakeven price (0–100). Defaults to 0. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "oil_breakeven_price_calculator",
  "arguments": {
    "lifting_cost_per_bbl": 0,
    "opex_per_bbl": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "oil_breakeven_price_calculator"`.
