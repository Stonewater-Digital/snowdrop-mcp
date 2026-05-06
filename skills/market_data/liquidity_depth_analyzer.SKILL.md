---
skill: liquidity_depth_analyzer
category: market_data
description: Estimates price impact and slippage for CFMM pools.
tier: free
inputs: pool_reserves, trade_size
---

# Liquidity Depth Analyzer

## Description
Estimates price impact and slippage for CFMM pools.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `pool_reserves` | `object` | Yes |  |
| `trade_size` | `number` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "liquidity_depth_analyzer",
  "arguments": {
    "pool_reserves": {},
    "trade_size": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "liquidity_depth_analyzer"`.
