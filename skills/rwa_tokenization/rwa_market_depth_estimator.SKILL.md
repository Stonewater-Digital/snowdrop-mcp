---
skill: rwa_market_depth_estimator
category: rwa_tokenization
description: Calculates average daily volume and depth to gauge token liquidity.
tier: free
inputs: daily_trades, outstanding_supply_usd
---

# Rwa Market Depth Estimator

## Description
Calculates average daily volume and depth to gauge token liquidity.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `daily_trades` | `array` | Yes | Recent daily trading stats |
| `outstanding_supply_usd` | `number` | Yes | Market cap of token |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "rwa_market_depth_estimator",
  "arguments": {
    "daily_trades": [],
    "outstanding_supply_usd": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rwa_market_depth_estimator"`.
