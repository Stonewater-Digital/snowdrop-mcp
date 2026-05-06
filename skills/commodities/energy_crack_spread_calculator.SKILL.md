---
skill: energy_crack_spread_calculator
category: commodities
description: Computes 3-2-1 crack spread (standard refinery margin), custom ratio crack spread, 1-1-1 simplified spread, and a margin compression flag. All prices in $/bbl.
tier: free
inputs: crude_price_per_bbl, gasoline_price_per_bbl, distillate_price_per_bbl
---

# Energy Crack Spread Calculator

## Description
Computes 3-2-1 crack spread (standard refinery margin), custom ratio crack spread, 1-1-1 simplified spread, and a margin compression flag. All prices in $/bbl.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `crude_price_per_bbl` | `number` | Yes | Crude oil input price per barrel (must be > 0). |
| `gasoline_price_per_bbl` | `number` | Yes | Gasoline (RBOB) price per barrel (must be > 0). |
| `distillate_price_per_bbl` | `number` | Yes | Distillate / heating oil / diesel price per barrel (must be > 0). |
| `gasoline_ratio` | `number` | No | Barrels of gasoline produced per N barrels of crude (default 2 in 3-2-1). |
| `distillate_ratio` | `number` | No | Barrels of distillate produced per N barrels of crude (default 1 in 3-2-1). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "energy_crack_spread_calculator",
  "arguments": {
    "crude_price_per_bbl": 0,
    "gasoline_price_per_bbl": 0,
    "distillate_price_per_bbl": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "energy_crack_spread_calculator"`.
