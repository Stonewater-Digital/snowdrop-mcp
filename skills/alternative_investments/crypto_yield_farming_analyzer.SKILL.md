---
skill: crypto_yield_farming_analyzer
category: alternative_investments
description: Converts pool volume/TVL and token incentives into APY while quantifying impermanent loss via volatility. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: tvl, trading_volume, fee_tier, token_emissions, token_price, asset_volatility
---

# Crypto Yield Farming Analyzer

## Description
Converts liquidity pool volume, TVL, and token incentives into APY while quantifying impermanent loss risk via underlying asset volatility. Supports fee-based and emission-based yield farming positions. Premium skill — subscribe at https://snowdrop.ai.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tvl` | `number` | Yes | Total value locked in the pool (dollars). |
| `trading_volume` | `number` | Yes | 24h trading volume through the pool (dollars). |
| `fee_tier` | `number` | Yes | Pool fee tier as a decimal (e.g. 0.003 for 0.3%). |
| `token_emissions` | `number` | Yes | Daily reward token emissions allocated to this pool. |
| `token_price` | `number` | Yes | Current reward token price (dollars). |
| `asset_volatility` | `number` | Yes | Annualized volatility of the pool's asset pair as a decimal (e.g. 0.80 for 80%). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "crypto_yield_farming_analyzer",
  "arguments": {
    "tvl": 5000000,
    "trading_volume": 800000,
    "fee_tier": 0.003,
    "token_emissions": 500,
    "token_price": 2.40,
    "asset_volatility": 0.85
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "crypto_yield_farming_analyzer"`.
