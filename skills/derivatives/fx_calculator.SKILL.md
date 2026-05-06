---
skill: fx_calculator
category: derivatives
description: Computes FX forward rates via covered interest parity and related metrics.
tier: free
inputs: spot_rate, domestic_rate_pct, foreign_rate_pct, days_to_maturity, notional_domestic
---

# Fx Calculator

## Description
Computes FX forward rates via covered interest parity and related metrics.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `spot_rate` | `number` | Yes | Spot FX rate (domestic per foreign unit, e.g. USD/EUR). Must be > 0. |
| `domestic_rate_pct` | `number` | Yes | Domestic interest rate as a percentage (simple, actual/360). |
| `foreign_rate_pct` | `number` | Yes | Foreign interest rate as a percentage (simple, actual/360). |
| `days_to_maturity` | `integer` | Yes | Number of days to forward delivery (must be >= 1). |
| `notional_domestic` | `number` | Yes | Domestic currency notional amount. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "fx_calculator",
  "arguments": {
    "spot_rate": 0,
    "domestic_rate_pct": 0,
    "foreign_rate_pct": 0,
    "days_to_maturity": 0,
    "notional_domestic": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "fx_calculator"`.
