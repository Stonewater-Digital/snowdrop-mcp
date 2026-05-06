---
skill: options_strategy_analyzer
category: derivatives
description: Aggregates multi-leg option strategy P&L and diagnostics.
tier: free
inputs: legs, spot_price
---

# Options Strategy Analyzer

## Description
Aggregates multi-leg option strategy P&L and diagnostics.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `legs` | `array` | Yes | Option legs with type, direction, strike, premium, quantity. |
| `spot_price` | `number` | Yes |  |
| `price_range_pct` | `number` | No | Symmetric percent band to sweep underlying prices. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "options_strategy_analyzer",
  "arguments": {
    "legs": [],
    "spot_price": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "options_strategy_analyzer"`.
