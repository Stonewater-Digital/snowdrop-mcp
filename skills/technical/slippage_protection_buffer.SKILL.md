---
skill: slippage_protection_buffer
category: technical
description: Calculate maximum allowable slippage for a trade using bid/ask spread and order book depth. Sets max_slippage = spread + estimated_impact + 10% buffer.
tier: free
inputs: order, market_data
---

# Slippage Protection Buffer

## Description
Calculate maximum allowable slippage for a trade using bid/ask spread and order book depth. Sets max_slippage = spread + estimated_impact + 10% buffer.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `order` | `object` | Yes | Order dict with: token_pair (str), amount_usd (float), side ('buy'/'sell'), exchange (str). |
| `market_data` | `object` | Yes | Market data dict with: bid (float), ask (float), depth_bps (list of {price_level, quantity}). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "slippage_protection_buffer",
  "arguments": {
    "order": {},
    "market_data": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "slippage_protection_buffer"`.
