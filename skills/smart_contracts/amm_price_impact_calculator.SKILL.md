---
skill: amm_price_impact_calculator
category: smart_contracts
description: Applies constant product math to measure price impact of swapping base for quote reserves.
tier: free
inputs: reserve_base, reserve_quote, trade_size_base
---

# Amm Price Impact Calculator

## Description
Applies constant product math to measure price impact of swapping base for quote reserves.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `reserve_base` | `number` | Yes | Current base asset reserve |
| `reserve_quote` | `number` | Yes | Current quote asset reserve |
| `trade_size_base` | `number` | Yes | Amount of base asset to sell into pool |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "amm_price_impact_calculator",
  "arguments": {
    "reserve_base": 0,
    "reserve_quote": 0,
    "trade_size_base": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "amm_price_impact_calculator"`.
