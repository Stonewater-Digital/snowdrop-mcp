---
skill: stock_to_flow_calculator
category: blockchain_analytics
description: Applies the PlanB stock-to-flow regression to estimate model price and scarcity context.
tier: free
inputs: circulating_supply, annual_production_rate, current_price
---

# Stock To Flow Calculator

## Description
Applies the PlanB stock-to-flow regression to estimate model price and scarcity context.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `circulating_supply` | `number` | Yes | Total circulating supply of the asset in native units. |
| `annual_production_rate` | `number` | Yes | Annualized new issuance of tokens or coins in native units. |
| `current_price` | `number` | Yes | Spot price of the asset in USD for deviation analysis. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "stock_to_flow_calculator",
  "arguments": {
    "circulating_supply": 0,
    "annual_production_rate": 0,
    "current_price": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "stock_to_flow_calculator"`.
