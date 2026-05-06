---
skill: fear_greed_composite
category: market_analytics
description: Combines multiple sentiment metrics into a 0-100 fear/greed composite score.
tier: free
inputs: market_momentum, market_breadth, put_call_ratio, junk_bond_demand, market_volatility, safe_haven_demand, stock_price_strength
---

# Fear Greed Composite

## Description
Combines multiple sentiment metrics into a 0-100 fear/greed composite score.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `market_momentum` | `number` | Yes | Momentum score (0-100). |
| `market_breadth` | `number` | Yes | Breadth score (0-100). |
| `put_call_ratio` | `number` | Yes | Inverse scaled PCR score (0-100). |
| `junk_bond_demand` | `number` | Yes | Risk appetite via HY demand. |
| `market_volatility` | `number` | Yes | Volatility score (lower vol => higher score). |
| `safe_haven_demand` | `number` | Yes | Demand for safe havens (inverse risk). |
| `stock_price_strength` | `number` | Yes | Percent of stocks above moving averages. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "fear_greed_composite",
  "arguments": {
    "market_momentum": 0,
    "market_breadth": 0,
    "put_call_ratio": 0,
    "junk_bond_demand": 0,
    "market_volatility": 0,
    "safe_haven_demand": 0,
    "stock_price_strength": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "fear_greed_composite"`.
