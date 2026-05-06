---
skill: defi_liquidity_pool_analyzer
category: smart_contracts
description: Computes turnover, fee APR, and concentration analytics for AMM pools.
tier: free
inputs: pool_liquidity_usd, volume_24h_usd, fee_bps, token_weights
---

# Defi Liquidity Pool Analyzer

## Description
Computes turnover, fee APR, and concentration analytics for AMM pools.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `pool_liquidity_usd` | `number` | Yes | Total liquidity value in USD |
| `volume_24h_usd` | `number` | Yes | Trailing 24h swap volume |
| `fee_bps` | `number` | Yes | Pool fee in basis points |
| `token_weights` | `array` | Yes | Constituent token weights for concentration review. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "defi_liquidity_pool_analyzer",
  "arguments": {
    "pool_liquidity_usd": 0,
    "volume_24h_usd": 0,
    "fee_bps": 0,
    "token_weights": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "defi_liquidity_pool_analyzer"`.
