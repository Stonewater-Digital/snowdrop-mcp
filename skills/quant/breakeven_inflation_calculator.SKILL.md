---
skill: breakeven_inflation_calculator
category: quant
description: Calculates breakeven inflation and adjusts for risk premium assumptions.
tier: free
inputs: nominal_yield_pct, tips_yield_pct
---

# Breakeven Inflation Calculator

## Description
Calculates breakeven inflation and adjusts for risk premium assumptions.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `nominal_yield_pct` | `number` | Yes |  |
| `tips_yield_pct` | `number` | Yes |  |
| `inflation_risk_premium_bps` | `number` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "breakeven_inflation_calculator",
  "arguments": {
    "nominal_yield_pct": 0,
    "tips_yield_pct": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "breakeven_inflation_calculator"`.
